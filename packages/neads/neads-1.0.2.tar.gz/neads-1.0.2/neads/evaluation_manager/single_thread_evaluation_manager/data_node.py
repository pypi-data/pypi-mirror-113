from __future__ import annotations

from typing import TYPE_CHECKING, Callable, Iterable, Any, Optional
from enum import Enum, auto
from collections import defaultdict
import copy as copy_module

from neads._internal_utils.object_temp_file import ObjectTempFile
import neads._internal_utils.memory_info as memory_info
from neads.database import DataNotFound

if TYPE_CHECKING:
    from neads.activation_model import SealedActivation
    from neads.database import IDatabase

import logging
logger = logging.getLogger('neads.data_node')


class DataNodeState(Enum):
    """State of the DataNode."""

    UNKNOWN = auto()
    NO_DATA = auto()
    MEMORY = auto()
    DISK = auto()


class DataNodeStateException(Exception):
    """For attempts to call DataNode's state-changing method in a wrong state.

    See docstring of DataNodes public methods for more information.
    """


class DataNode:
    """Node in EvaluationState for a single Activation in ActivationGraph.

    DataNode represents data of a single Activation. It is in one of the
    following states: UNKNOWN, NO_DATA, MEMORY, DISK. These states are
    represented by the values of enum DataNodeState.

    In UNKNOWN state, we do not know yet whether we already have the data or
    not. We need to check it first (to database, if there is any) via method
    try_load().

    In NO_DATA state, we know that we do not have the data. If the user wants
    them, they must be computed via evaluate() method.

    In MEMORY state, the node data are in memory. If it is necessary to release
    some memory, the data may be moved to disk via store() method.

    In DISK state, the data are on disk. If they need to become active
    (usually because a child of the node is meant to be evaluated), the data
    may be moved to memory via load() method.

    For more detail on the methods, see their docstring.
    """

    _OBJECT_TEMP_FILE_PROVIDER = ObjectTempFile

    def __init__(self,
                 activation: SealedActivation,
                 parents: Iterable[DataNode],
                 database: IDatabase):
        """Initialize a DataNode instance.

        The initial state is UNKNOWN.

        Parameters
        ----------
        activation
            The Activation whose data and state the DataNode instance
            represents.
        parents
            Parent DataNodes of the created instance.
        database
            Database for Activation's data. The DataNode will try to load its
            data from the database or save it there after evaluation
            (in case the data was not found). The database is expected to be
            open when calling the `try_load` method.
        """

        self._activation: SealedActivation = activation
        self._parents: Iterable[DataNode] = parents
        self._children: list[DataNode] = []
        self._state: DataNodeState = DataNodeState.UNKNOWN

        self._data: Optional[Any] = None
        self._data_size: Optional[int] = None

        self._database: IDatabase = database
        self._temp_file: Optional[ObjectTempFile] = None

        self._callbacks: \
            dict[tuple[DataNodeState, DataNodeState],
                 list[Callable[[DataNode], None]]] \
            = defaultdict(list)

        for parent in self._parents:
            parent._children.append(self)

        logger.info(f'Created node: {self}.')

    @property
    def activation(self):
        """The activation represented by the node."""
        return self._activation

    @property
    def state(self):
        """State of the DataNode."""
        return self._state

    @property
    def level(self):
        """Return level of the DataNode in the graph.

        The level is determined as the maximum of levels of parents + 1.
        The DataNode without parents have level 0.

        Returns
        -------
            Level of the DateNode.
        """

        return self._activation.level

    @property
    def parents(self):
        """Parent nodes of the DataNode.

        The relations child-parent corresponds to the underlying
        ActivationGraph.
        """

        return self._parents

    @property
    def children(self):
        """Child nodes of the DataNode.

        The relations child-parent corresponds to the underlying
        ActivationGraph.
        """

        return self._children

    @property
    def has_trigger_on_result(self):
        """Whether the corresponding Activation has trigger-on_result."""

        return self._activation.trigger_on_result is not None

    @property
    def has_trigger_on_descendants(self):
        """Whether the corresponding Activation has trigger-on-descendants."""

        return self._activation.trigger_on_descendants is not None

    @property
    def data_size(self):
        """Size of the actual data in bytes, if it is known.

        The size is not known in UNKNOWN and NO_DATA state and None is returned.
        Also note that in DISK state the size is known, but the data of such
        size are not in memory but only on disk (more precisely, it depends
        on the behavior of GC and the Database).
        """

        return self._data_size

    def get_data(self, *, copy=True):
        """The data of the node.

        Parameters
        ----------
        copy
            Whether only a copy of the data is returned.

        Returns
        -------
            The node's data or their deepcopy, if the node is in MEMORY state.
            Otherwise None.

        Notes
        -----
            Changing the actual data is hugely discouraged, as some future
            results may depend on these data. The change then leads to
            undefined behavior.
        """

        # If the state is not MEMORY, value is self._data is None
        if copy:
            return copy_module.deepcopy(self._data)
        else:
            return self._data

    def try_load(self) -> bool:
        """Try load the data from database.

        Allowed only in UNKNOWN state. There are two possible results. Either
        the attempt to load the data was successful and the state changes to
        MEMORY. Or, in case the attempt was not successful, the state changes
        to NO_DATA.

        The given database is expected to be open when calling the `try_load`
        method.

        Returns
        -------
            True, it the attempt to load was successful. False otherwise.

        Raises
        ------
        DataNodeStateException
            If the DataNode is in different state than UNKNOWN.
        """

        logger.debug(f'Trying to load: {self}.')

        self._check_appropriate_state(DataNodeState.UNKNOWN)
        try:
            self._data = self._database.load(self._activation.definition)
            self._data_size = memory_info.get_object_size(self._data)
            self._change_state(DataNodeState.MEMORY)
            logger.debug(f'Data found: {self}.')
            return True
        except DataNotFound:
            self._change_state(DataNodeState.NO_DATA)
            logger.debug(f'Data not found: {self}.')
            return False

    def evaluate(self):
        """Evaluate the data.

        Allowed only in NO_DATA state and the resulting state is MEMORY.
        The method calls the corresponding plugin with appropriate arguments.
        The parent nodes MUST be in MEMORY state when calling evaluate().

        Raises
        ------
        DataNodeStateException
            If the DataNode is in different state than NO_DATA.
        RuntimeError
            A parent node was not in MEMORY state.
        PluginException
            When the plugin raises an exception.
        """

        logger.debug(f'Evaluating: {self}.')

        # Initial state checks
        self._check_appropriate_state(DataNodeState.NO_DATA)
        for parent in self._parents:
            if parent.state is not DataNodeState.MEMORY:
                raise RuntimeError(
                    f'Parent node {parent} is not in MEMORY state'
                )

        # Creating the actual argument set
        symbol_to_data_map = {
            parent._activation.symbol: parent._data
            for parent in self._parents
        }
        argument_set = self._activation.argument_set.get_actual_arguments(
            symbol_to_data_map
        )

        # Getting plugin and computing its result
        plugin = self._activation.plugin
        self._data = plugin(*argument_set.args, **argument_set.kwargs)

        # Finishing the state-transition
        self._database.save(self._data, self._activation.definition)
        self._data_size = memory_info.get_object_size(self._data)
        self._change_state(DataNodeState.MEMORY)

        logger.debug(f'Evaluation finished: {self}.')
        # Two log (start and end) are there due to possible low speed of eval 

    def store(self):
        """Store data on disk.

        Allowed only in MEMORY state and the resulting state is DISK. It stores
        the data to tmp file and releases the pointer to the data instance.

        Raises
        ------
        DataNodeStateException
            If the DataNode is in different state than MEMORY.
        """

        logger.debug(f'Storing data to disk: {self}.')

        self._check_appropriate_state(DataNodeState.MEMORY)
        if self._temp_file is None:
            self._temp_file = self._OBJECT_TEMP_FILE_PROVIDER()
        self._temp_file.save(self._data)
        self._data = None  # Releasing reference, so GC can collect

        self._change_state(DataNodeState.DISK)

    def load(self):
        """Load data to memory.

        Allowed only in DISK state and the resulting state is MEMORY. Data
        are loaded from tmp file to memory.

        Raises
        ------
        DataNodeStateException
            If the DataNode is in different state than DISK.
        """

        logger.debug(f'Loading data to memory: {self}.')

        self._check_appropriate_state(DataNodeState.DISK)
        self._data = self._temp_file.load()

        self._change_state(DataNodeState.MEMORY)

    def register_callback_unknown_to_no_data(
            self, callback: Callable[[DataNode], None]):
        """Register callback for change of state from UNKNOWN to NO_DATA.

        Parameters
        ----------
        callback
            The callback to be called after change of state from UNKNOWN to
            NO_DATA with a single argument, which is the DataNode.
        """

        self._register_callback(
            DataNodeState.UNKNOWN,
            DataNodeState.NO_DATA,
            callback
        )

    def register_callback_unknown_to_memory(
            self, callback: Callable[[DataNode], None]):
        """Register callback for change of state from UNKNOWN to MEMORY.

        Parameters
        ----------
        callback
            The callback to be called after change of state from UNKNOWN to
            MEMORY with a single argument, which is the DataNode.
        """

        self._register_callback(
            DataNodeState.UNKNOWN,
            DataNodeState.MEMORY,
            callback
        )

    def register_callback_no_data_to_memory(
            self, callback: Callable[[DataNode], None]):
        """Register callback for change of state from NO_DATA to MEMORY.

        Parameters
        ----------
        callback
            The callback to be called after change of state from NO_DATA to
            MEMORY with a single argument, which is the DataNode.
        """

        self._register_callback(
            DataNodeState.NO_DATA,
            DataNodeState.MEMORY,
            callback
        )

    def register_callback_memory_to_disk(
            self, callback: Callable[[DataNode], None]):
        """Register callback for change of state from MEMORY to DISK.

        Parameters
        ----------
        callback
            The callback to be called after change of state from MEMORY to
            DISK with a single argument, which is the DataNode.
        """

        self._register_callback(
            DataNodeState.MEMORY,
            DataNodeState.DISK,
            callback
        )

    def register_callback_disk_to_memory(
            self, callback: Callable[[DataNode], None]):
        """Register callback for change of state from DISK to MEMORY.

        Parameters
        ----------
        callback
            The callback to be called after change of state from DISK to
            MEMORY with a single argument, which is the DataNode.
        """

        self._register_callback(
            DataNodeState.DISK,
            DataNodeState.MEMORY,
            callback
        )

    def _call_callbacks(
            self, callback_list: Iterable[Callable[[DataNode], None]]):
        """Call all callbacks from the given callbacks list.

        Parameters
        ----------
        callback_list
            The list of callbacks to be called.
        """

        for callback in callback_list:
            callback(self)

    def _check_appropriate_state(self, expected_state: DataNodeState):
        """Check that the actual DataNode's state corresponds to expected state.

        Parameters
        ----------
        expected_state
            Expected state of the DataNode.

        Raises
        -------
        DataNodeStateException
            If the actual state differs from the expected state.
        """

        if expected_state is not self._state:
            raise DataNodeStateException(
                f'The DataNode is in state {self.state} while '
                f'{expected_state} is expected'
            )

    def _register_callback(self, state_from, state_to, callback):
        """Register a callback for transition between the given states.

        Parameters
        ----------
        state_from
            State from which the transition must lead for calling the callback.
        state_to
            State to which which the transition must lead for calling the
            callback.
        callback
            The new callback method to be registered.
        """

        self._callbacks[(state_from, state_to)].append(callback)

    def _change_state(self, state_to):
        """Change state from current to the given.

        It changes the value of self._state and do associated work (e.g.
        calling appropriate callbacks).

        Parameters
        ----------
        state_to
            The new state of the DataNode.
        """

        state_from = self._state
        self._state = state_to
        callback_list = self._callbacks[(state_from, state_to)]
        self._call_callbacks(callback_list)

    def __str__(self):
        return f'DataNode({self.activation.plugin.id},' \
               f' {self._activation.argument_set})'

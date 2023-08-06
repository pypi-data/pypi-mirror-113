from neads.activation_model import ActivationGraph


def get_result_activation(graph: ActivationGraph):
    """Check that the graph has exactly one result Activation and return it.

    Activation is regarded as the 'result Activation' iff it is childless.

    Parameters
    ----------
    graph
        The graph whose result Activation is returned.

    Returns
    -------
        The result Activation of the given graph.

    Raises
    ------
    ValueError
        If the graph does not have exactly one result Activation.
    """

    result_acts = [act for act in graph if not act.children]
    if len(result_acts) == 1:
        return result_acts[0]
    else:
        raise ValueError(
            f'The graph does not have one result Activation: {result_acts}'
        )


def assert_no_triggers(graph: ActivationGraph):
    """Assert that the graph has no trigger (graph's nor Activations').

    Parameters
    ----------
    graph
        The examined graph.

    Raises
    ------
    ValueError
        If the graph or one of its Activations has a trigger method.
    """

    has_graph_trigger = bool(graph.trigger_method)
    has_trigger_on_result = bool([act for act in graph
                                  if act.trigger_on_result])
    has_trigger_on_descendants = bool([act for act in graph
                                       if act.trigger_on_descendants])

    if has_graph_trigger or has_trigger_on_result or has_trigger_on_descendants:
        raise ValueError('The graph contains a trigger method')


def assert_inputs_count(graph: ActivationGraph, expected: int):
    """Assert that the graph has the given number of inputs.

    Parameters
    ----------
    graph
        The examined graph.
    expected
        The expected number of inputs.

    Raises
    ------
    ValueError
        If the graph has different number of inputs than expected.
    """

    number_of_inputs = len(graph.inputs)
    if number_of_inputs != expected:
        raise ValueError(f"The number of graph's inputs ({number_of_inputs}) "
                         f"differs from the expected ({expected})")

from typing import Callable

import pp
from pp.component import Component
from pp.components.electrical.pad import pad_array
from pp.routing.get_route import get_route_from_waypoints
from pp.routing.get_route_electrical_shortest_path import (
    get_route_electrical_shortest_path,
)
from pp.routing.sort_ports import sort_ports


@pp.cell_with_validator
def add_electrical_pads_top(
    component: Component,
    component_top_to_pad_bottom_distance: float = 100.0,
    route_filter: Callable = get_route_from_waypoints,
    **kwargs,
) -> Component:
    """Returns new component with electrical ports connected to top pad array

    Args:
        component:
        pad: pad element
        spacing: pad array (x, y) spacing
        width: pad width
        height: pad height
        layer: pad layer
    """
    c = Component()
    ports = component.get_ports_list(port_type="dc")
    c << component
    pads = c << pad_array(n=len(ports), port_list=["S"], **kwargs)
    pads.x = component.x
    pads.ymin = component.ymax + component_top_to_pad_bottom_distance
    ports_pads = list(pads.ports.values())

    # ports_pads.sort(key=lambda p: p.midpoint[0])
    # ports.sort(key=lambda p: p.midpoint[0])

    ports_pads, ports = sort_ports(ports_pads, ports)

    for p1, p2 in zip(ports_pads, ports):
        c.add(get_route_electrical_shortest_path(p1, p2))

    c.ports = component.ports.copy()
    for port in ports:
        c.ports.pop(port.name)
    return c


if __name__ == "__main__":
    import pp

    c = pp.components.straight_with_heater()
    c = pp.components.mzi2x2(with_elec_connections=True)
    cc = add_electrical_pads_top(component=c)
    cc.show()

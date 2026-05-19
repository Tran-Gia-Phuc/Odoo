/** @odoo-module */

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MyHeader extends Component {
    static template = "zoo.MyHeader";
    setup() {  
        // lấy field name từ record hiện tại
        const rec = this.props.record ? this.props.record.data : false;

        this.state = useState({
            name: rec ? rec.name : "No Name",
        });
    };

    on_click() {
        alert("Animal name: " + this.state.name);
    }
}

export const myheader = {
    component: MyHeader,
};

registry.category("view_widgets").add("myheader", myheader);
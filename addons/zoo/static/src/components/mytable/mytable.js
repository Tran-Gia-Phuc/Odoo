/** @odoo-module */

// dòng trên là bắt buộc để khai báo một custom module trong Odoo => để code có thể dịch theo owl js thay vì javascript thông thường
// nếu có không sẽ báo lỗi:
// "Uncaught SyntaxError: Cannot use import statement outside a module"
// Ref: https://dev.to/jeevanizm/uncaught-syntaxerror-cannot-use-import-statement-outside-a-module-34cc

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MyTableWidget extends Component {
    static template = "zoo.MyTable";
    setup() {   // khởi tạo "component" này
        const rec = this.props.record ? this.props.record.data : false;
        var prop_arr = [];        
        for (var key in rec) {
            if (rec.hasOwnProperty(key)) {
                var value = rec[key];
                if (typeof value === 'object' && value !== null) {
                    value = value.id;
                }
                //console.log(key + " -> " + this.data[key]);
                if (value == undefined) {
                    continue;
                }
                var prop_data = {
                    "key": key,
                    "value": value,
                };
                prop_arr.push(prop_data);
            }
        }
        this.state = useState({
          title: "My Table OWL",
          data_prop: prop_arr,
          rec: rec
        });
        
        console.log("HighlightTextWidget @ this");
        console.log(this);  
        
        //...
		// thêm các code sau vào cuối hàm setup()
        this.orm = useService("orm");
        const result = this.orm.call("zoo.animal", "get_table_title", [], {
            value: "minhng.info",
        }); // it's an object promise
        var self = this;
        result.then((title_from_server) => {
            self.state.title = title_from_server;
        });  
    }

    title_clicked() {
        alert("Clicked on \"" + this.state.title + "\" title :)~");
    }
}

export const mytablewidget = {
    component: MyTableWidget,
};

registry.category("view_widgets").add("mytable", mytablewidget);  // usage: <widget name="mytable"/>
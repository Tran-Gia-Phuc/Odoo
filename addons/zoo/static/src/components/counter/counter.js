/** @odoo-module */

// dòng trên là bắt buộc để khai báo một custom module trong Odoo => để code có thể dịch theo owl js thay vì javascript thông thường
// nếu có không sẽ báo lỗi:
// "Uncaught SyntaxError: Cannot use import statement outside a module"
// Ref: https://dev.to/jeevanizm/uncaught-syntaxerror-cannot-use-import-statement-outside-a-module-34cc

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

function getTodayAsInteger() {
    const today = new Date();
    const year = String(today.getFullYear()).slice(-2);
    const month = String(today.getMonth() + 1).padStart(2, '0'); // Months are zero-based
    const day = String(today.getDate()).padStart(2, '0');

    return parseInt(`${year}${month}${day}`, 10);
}

const X = 10;
const Y = 100;

function getRandomValue(x, y) {
    return Math.floor(Math.random() * (y - x + 1)) + x;
}
function increase(value) {
    value = value < Y ? value + 1 : X;
    return value;
}

function decrease(value) {
    value = value > X ? value - 1 : Y;
    return value;
}


export class Counter extends Component {
    static template = "zoo.counter";

    setup() {   // khởi tạo "component" này
        this.state = useState({ value: getTodayAsInteger() });  // example: 241210
    }

    increment() {     // định nghĩa phương thức / hành động của "component"
        this.state.value++;
    }
}

export class Exercise extends Component {
    static template = "zoo.exercise";

    setup() {
        this.state = useState({
            value: getRandomValue(X, Y),
        });
    }

    increase() {
        this.state.value =
            this.state.value < Y ? this.state.value + 1 : X;
    }

    decrease() {
        this.state.value =
            this.state.value > X ? this.state.value - 1 : Y;
    }
}


export const counter = {
    component: Counter,Exercise
};

registry.category("view_widgets").add("counter", counter);  // usage: <widget name="counter"/>
registry.category("view_widgets").add("exercise", {component: Exercise,});  // usage: <widget name="exercise"/>

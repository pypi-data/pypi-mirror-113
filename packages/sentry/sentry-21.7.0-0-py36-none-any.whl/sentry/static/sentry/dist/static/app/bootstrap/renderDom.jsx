Object.defineProperty(exports, "__esModule", { value: true });
exports.renderDom = void 0;
var tslib_1 = require("tslib");
var react_1 = tslib_1.__importDefault(require("react"));
var react_dom_1 = tslib_1.__importDefault(require("react-dom"));
function renderDom(Component, container, props) {
    if (props === void 0) { props = {}; }
    var rootEl = document.querySelector(container);
    // Note: On pages like `SetupWizard`, we will attempt to mount main App
    // but will fail because the DOM el wasn't found (which is intentional)
    if (!rootEl) {
        return;
    }
    react_dom_1.default.render(<Component {...props}/>, rootEl);
}
exports.renderDom = renderDom;
//# sourceMappingURL=renderDom.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
function ConfirmableAction(_a) {
    var shouldConfirm = _a.shouldConfirm, children = _a.children, props = tslib_1.__rest(_a, ["shouldConfirm", "children"]);
    if (shouldConfirm) {
        return <confirm_1.default {...props}>{children}</confirm_1.default>;
    }
    return <React.Fragment>{children}</React.Fragment>;
}
exports.default = ConfirmableAction;
//# sourceMappingURL=confirmableAction.jsx.map
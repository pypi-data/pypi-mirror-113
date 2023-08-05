Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var mobx_react_1 = require("mobx-react");
var state_1 = tslib_1.__importDefault(require("app/components/forms/state"));
var controlState_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/controlState"));
/**
 * ControlState (i.e. loading/error icons) for connected form components
 */
var FormFieldControlState = function (_a) {
    var model = _a.model, name = _a.name;
    return (<mobx_react_1.Observer>
    {function () {
            var isSaving = model.getFieldState(name, state_1.default.SAVING);
            var isSaved = model.getFieldState(name, state_1.default.READY);
            var error = model.getError(name);
            return <controlState_1.default isSaving={isSaving} isSaved={isSaved} error={error}/>;
        }}
  </mobx_react_1.Observer>);
};
exports.default = FormFieldControlState;
//# sourceMappingURL=controlState.jsx.map
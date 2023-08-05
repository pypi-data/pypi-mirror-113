Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var locale_1 = require("app/locale");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var ConfirmDelete = function (_a) {
    var message = _a.message, confirmInput = _a.confirmInput, props = tslib_1.__rest(_a, ["message", "confirmInput"]);
    return (<confirm_1.default {...props} bypass={false} disableConfirmButton renderMessage={function (_a) {
            var disableConfirmButton = _a.disableConfirmButton;
            return (<React.Fragment>
        <alert_1.default type="error">{message}</alert_1.default>
        <field_1.default flexibleControlStateSize inline={false} label={locale_1.t('Please enter %s to confirm the deletion', <code>{confirmInput}</code>)}>
          <input_1.default type="text" placeholder={confirmInput} onChange={function (e) { return disableConfirmButton(e.target.value !== confirmInput); }}/>
        </field_1.default>
      </React.Fragment>);
        }}/>);
};
exports.default = ConfirmDelete;
//# sourceMappingURL=confirmDelete.jsx.map
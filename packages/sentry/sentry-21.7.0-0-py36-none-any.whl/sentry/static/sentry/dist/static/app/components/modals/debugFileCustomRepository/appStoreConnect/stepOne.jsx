Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var textarea_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/textarea"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
function StepOne(_a) {
    var stepOneData = _a.stepOneData, onSetStepOneData = _a.onSetStepOneData;
    return (<react_1.Fragment>
      <field_1.default label={locale_1.t('Issuer')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="issuer" placeholder={locale_1.t('Issuer')} value={stepOneData.issuer} onChange={function (e) {
            return onSetStepOneData(tslib_1.__assign(tslib_1.__assign({}, stepOneData), { issuer: e.target.value }));
        }}/>
      </field_1.default>
      <field_1.default label={locale_1.t('Key ID')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="keyId" placeholder={locale_1.t('Key Id')} value={stepOneData.keyId} onChange={function (e) {
            return onSetStepOneData(tslib_1.__assign(tslib_1.__assign({}, stepOneData), { keyId: e.target.value }));
        }}/>
      </field_1.default>
      <field_1.default label={locale_1.t('Private Key')} inline={false} flexibleControlStateSize stacked required>
        <textarea_1.default name="privateKey" placeholder={locale_1.t('Private Key')} value={stepOneData.privateKey} rows={5} autosize onChange={function (e) {
            return onSetStepOneData(tslib_1.__assign(tslib_1.__assign({}, stepOneData), { privateKey: e.target.value }));
        }}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepOne;
//# sourceMappingURL=stepOne.jsx.map
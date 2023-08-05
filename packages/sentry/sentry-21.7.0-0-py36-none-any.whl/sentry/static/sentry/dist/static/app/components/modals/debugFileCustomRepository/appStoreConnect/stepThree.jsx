Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var locale_1 = require("app/locale");
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
function StepThree(_a) {
    var stepThreeData = _a.stepThreeData, onSetStepOneData = _a.onSetStepOneData;
    return (<react_1.Fragment>
      <field_1.default label={locale_1.t('Username')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="text" name="username" placeholder={locale_1.t('Username')} onChange={function (e) { return onSetStepOneData(tslib_1.__assign(tslib_1.__assign({}, stepThreeData), { username: e.target.value })); }}/>
      </field_1.default>
      <field_1.default label={locale_1.t('Password')} inline={false} flexibleControlStateSize stacked required>
        <input_1.default type="password" name="password" placeholder={locale_1.t('Password')} onChange={function (e) { return onSetStepOneData(tslib_1.__assign(tslib_1.__assign({}, stepThreeData), { password: e.target.value })); }}/>
      </field_1.default>
    </react_1.Fragment>);
}
exports.default = StepThree;
//# sourceMappingURL=stepThree.jsx.map
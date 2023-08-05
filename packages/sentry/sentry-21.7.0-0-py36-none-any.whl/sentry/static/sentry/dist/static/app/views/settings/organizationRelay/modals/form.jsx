var _this = this;
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var input_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/input"));
var textarea_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/controls/textarea"));
var field_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field"));
var fieldHelp_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/field/fieldHelp"));
var textCopyInput_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/textCopyInput"));
var Form = function (_a) {
    var values = _a.values, onChange = _a.onChange, errors = _a.errors, onValidate = _a.onValidate, isFormValid = _a.isFormValid, disables = _a.disables, onValidateKey = _a.onValidateKey, onSave = _a.onSave;
    var handleChange = function (field) {
        return function (event) {
            onChange(field, event.target.value);
        };
    };
    var handleSubmit = function () {
        if (isFormValid) {
            onSave();
        }
    };
    // code below copied from app/views/organizationIntegrations/SplitInstallationIdModal.tsx
    // TODO: fix the common method selectText
    var onCopy = function (value) { return function () { return tslib_1.__awaiter(_this, void 0, void 0, function () { return tslib_1.__generator(this, function (_a) {
        switch (_a.label) {
            case 0: 
            // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [4 /*yield*/, navigator.clipboard.writeText(value)];
            case 1: 
            // This hack is needed because the normal copying methods with TextCopyInput do not work correctly
            return [2 /*return*/, _a.sent()];
        }
    }); }); }; };
    return (<form onSubmit={handleSubmit} id="relay-form">
      <field_1.default flexibleControlStateSize label={locale_1.t('Display Name')} error={errors.name} inline={false} stacked required>
        <input_1.default type="text" name="name" placeholder={locale_1.t('Display Name')} onChange={handleChange('name')} value={values.name} onBlur={onValidate('name')} disabled={disables.name}/>
      </field_1.default>

      {disables.publicKey ? (<field_1.default flexibleControlStateSize label={locale_1.t('Public Key')} inline={false} stacked>
          <textCopyInput_1.default onCopy={onCopy(values.publicKey)}>
            {values.publicKey}
          </textCopyInput_1.default>
        </field_1.default>) : (<FieldWrapper>
          <StyledField label={locale_1.t('Public Key')} error={errors.publicKey} flexibleControlStateSize inline={false} stacked required>
            <input_1.default type="text" name="publicKey" placeholder={locale_1.t('Public Key')} onChange={handleChange('publicKey')} value={values.publicKey} onBlur={onValidateKey}/>
          </StyledField>
          <fieldHelp_1.default>
            {locale_1.t('Only enter the Public Key value from your credentials file. Never share the Secret key with Sentry or any third party')}
          </fieldHelp_1.default>
        </FieldWrapper>)}
      <field_1.default flexibleControlStateSize label={locale_1.t('Description')} inline={false} stacked>
        <textarea_1.default name="description" placeholder={locale_1.t('Description')} onChange={handleChange('description')} value={values.description} disabled={disables.description} autosize/>
      </field_1.default>
    </form>);
};
exports.default = Form;
var FieldWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding-bottom: ", ";\n"], ["\n  padding-bottom: ", ";\n"])), space_1.default(2));
var StyledField = styled_1.default(field_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-bottom: 0;\n"], ["\n  padding-bottom: 0;\n"])));
var templateObject_1, templateObject_2;
//# sourceMappingURL=form.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var panels_1 = require("app/components/panels");
var accountPassword_1 = tslib_1.__importDefault(require("app/data/forms/accountPassword"));
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
function PasswordForm() {
    function handleSubmitSuccess(_change, model) {
        // Reset form on success
        model.resetForm();
        indicator_1.addSuccessMessage('Password has been changed');
    }
    function handleSubmitError() {
        indicator_1.addErrorMessage('Error changing password');
    }
    var user = configStore_1.default.get('user');
    return (<form_1.default apiMethod="PUT" apiEndpoint="/users/me/password/" initialData={{}} onSubmitSuccess={handleSubmitSuccess} onSubmitError={handleSubmitError} hideFooter>
      <jsonForm_1.default forms={accountPassword_1.default} additionalFieldProps={{ user: user }} renderFooter={function () { return (<Actions>
            <button_1.default type="submit" priority="primary">
              {locale_1.t('Change password')}
            </button_1.default>
          </Actions>); }} renderHeader={function () { return (<panels_1.PanelAlert type="info">
            {locale_1.t('Changing your password will invalidate all logged in sessions.')}
          </panels_1.PanelAlert>); }}/>
    </form_1.default>);
}
var Actions = styled_1.default(panels_1.PanelItem)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-end;\n"], ["\n  justify-content: flex-end;\n"])));
exports.default = PasswordForm;
var templateObject_1;
//# sourceMappingURL=passwordForm.jsx.map
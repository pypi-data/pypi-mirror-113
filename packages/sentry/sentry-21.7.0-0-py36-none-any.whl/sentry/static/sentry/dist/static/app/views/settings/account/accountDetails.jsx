Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var account_1 = require("app/actionCreators/account");
var avatarChooser_1 = tslib_1.__importDefault(require("app/components/avatarChooser"));
var accountDetails_1 = tslib_1.__importDefault(require("app/data/forms/accountDetails"));
var accountPreferences_1 = tslib_1.__importDefault(require("app/data/forms/accountPreferences"));
var locale_1 = require("app/locale");
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var jsonForm_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/jsonForm"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var ENDPOINT = '/users/me/';
var AccountDetails = /** @class */ (function (_super) {
    tslib_1.__extends(AccountDetails, _super);
    function AccountDetails() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSubmitSuccess = function (user) {
            // the updateUser method updates our Config Store
            // No components listen to the ConfigStore, they just access it directly
            account_1.updateUser(user);
            // We need to update the state, because AvatarChooser is using it,
            // otherwise it will flick
            _this.setState({
                user: user,
            });
        };
        return _this;
    }
    AccountDetails.prototype.getEndpoints = function () {
        // local state is NOT updated when the form saves
        return [['user', ENDPOINT]];
    };
    AccountDetails.prototype.renderBody = function () {
        var _this = this;
        var user = this.state.user;
        var formCommonProps = {
            apiEndpoint: ENDPOINT,
            apiMethod: 'PUT',
            allowUndo: true,
            saveOnBlur: true,
            onSubmitSuccess: this.handleSubmitSuccess,
        };
        return (<div>
        <settingsPageHeader_1.default title={locale_1.t('Account Details')}/>
        <form_1.default initialData={user} {...formCommonProps}>
          <jsonForm_1.default forms={accountDetails_1.default} additionalFieldProps={{ user: user }}/>
        </form_1.default>
        <form_1.default initialData={user.options} {...formCommonProps}>
          <jsonForm_1.default forms={accountPreferences_1.default} additionalFieldProps={{ user: user }}/>
        </form_1.default>
        <avatarChooser_1.default endpoint="/users/me/avatar/" model={user} onSave={function (resp) {
                _this.handleSubmitSuccess(resp);
            }} isUser/>
      </div>);
    };
    return AccountDetails;
}(asyncView_1.default));
exports.default = AccountDetails;
//# sourceMappingURL=accountDetails.jsx.map
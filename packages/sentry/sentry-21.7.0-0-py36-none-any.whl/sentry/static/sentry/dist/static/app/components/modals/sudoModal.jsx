Object.defineProperty(exports, "__esModule", { value: true });
exports.SudoModal = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var u2fContainer_1 = tslib_1.__importDefault(require("app/components/u2f/u2fContainer"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var form_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/form"));
var inputField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/inputField"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var SudoModal = /** @class */ (function (_super) {
    tslib_1.__extends(SudoModal, _super);
    function SudoModal() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            error: false,
            busy: false,
        };
        _this.handleSuccess = function () {
            var _a = _this.props, closeModal = _a.closeModal, superuser = _a.superuser, location = _a.location, router = _a.router, retryRequest = _a.retryRequest;
            if (!retryRequest) {
                closeModal();
                return;
            }
            if (superuser) {
                router.replace({ pathname: location.pathname, state: { forceUpdate: new Date() } });
                return;
            }
            _this.setState({ busy: true }, function () {
                retryRequest().then(function () {
                    _this.setState({ busy: false }, closeModal);
                });
            });
        };
        _this.handleError = function () {
            _this.setState({ busy: false, error: true });
        };
        _this.handleU2fTap = function (data) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var api, err_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        this.setState({ busy: true });
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/', { method: 'PUT', data: data })];
                    case 2:
                        _a.sent();
                        this.handleSuccess();
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _a.sent();
                        this.setState({ busy: false });
                        // u2fInterface relies on this
                        throw err_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    SudoModal.prototype.renderBodyContent = function () {
        var superuser = this.props.superuser;
        var error = this.state.error;
        var user = configStore_1.default.get('user');
        if (!user.hasPasswordAuth) {
            return (<React.Fragment>
          <textBlock_1.default>{locale_1.t('You will need to reauthenticate to continue.')}</textBlock_1.default>
          <button_1.default priority="primary" href={"/auth/login/?next=" + encodeURIComponent(location.pathname)}>
            {locale_1.t('Continue')}
          </button_1.default>
        </React.Fragment>);
        }
        return (<React.Fragment>
        <StyledTextBlock>
          {superuser
                ? locale_1.t('You are attempting to access a resource that requires superuser access, please re-authenticate as a superuser.')
                : locale_1.t('Help us keep your account safe by confirming your identity.')}
        </StyledTextBlock>

        {error && (<StyledAlert type="error" icon={<icons_1.IconFlag size="md"/>}>
            {locale_1.t('Incorrect password')}
          </StyledAlert>)}

        <form_1.default apiMethod="PUT" apiEndpoint="/auth/" submitLabel={locale_1.t('Confirm Password')} onSubmitSuccess={this.handleSuccess} onSubmitError={this.handleError} hideFooter={!user.hasPasswordAuth} resetOnError>
          <StyledInputField type="password" inline={false} label={locale_1.t('Password')} name="password" autoFocus flexibleControlStateSize/>
          <u2fContainer_1.default displayMode="sudo" onTap={this.handleU2fTap}/>
        </form_1.default>
      </React.Fragment>);
    };
    SudoModal.prototype.render = function () {
        var _a = this.props, Header = _a.Header, Body = _a.Body;
        return (<React.Fragment>
        <Header closeButton>{locale_1.t('Confirm Password to Continue')}</Header>
        <Body>{this.renderBodyContent()}</Body>
      </React.Fragment>);
    };
    return SudoModal;
}(React.Component));
exports.SudoModal = SudoModal;
exports.default = react_router_1.withRouter(withApi_1.default(SudoModal));
var StyledTextBlock = styled_1.default(textBlock_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
var StyledInputField = styled_1.default(inputField_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-left: 0;\n"], ["\n  padding-left: 0;\n"])));
var StyledAlert = styled_1.default(alert_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  margin-bottom: 0;\n"], ["\n  margin-bottom: 0;\n"])));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=sudoModal.jsx.map
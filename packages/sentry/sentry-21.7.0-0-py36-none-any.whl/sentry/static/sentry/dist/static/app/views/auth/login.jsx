Object.defineProperty(exports, "__esModule", { value: true });
exports.formFooterClass = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var loginForm_1 = tslib_1.__importDefault(require("./loginForm"));
var registerForm_1 = tslib_1.__importDefault(require("./registerForm"));
var ssoForm_1 = tslib_1.__importDefault(require("./ssoForm"));
var FORM_COMPONENTS = {
    login: loginForm_1.default,
    register: registerForm_1.default,
    sso: ssoForm_1.default,
};
var Login = /** @class */ (function (_super) {
    tslib_1.__extends(Login, _super);
    function Login() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            loading: true,
            error: null,
            activeTab: 'login',
            authConfig: null,
        };
        _this.handleSetTab = function (activeTab, event) {
            _this.setState({ activeTab: activeTab });
            event.preventDefault();
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var api, response, vsts_login_link, github_login_link, google_login_link, config, authConfig, e_1;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0:
                        api = this.props.api;
                        _a.label = 1;
                    case 1:
                        _a.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, api.requestPromise('/auth/config/')];
                    case 2:
                        response = _a.sent();
                        vsts_login_link = response.vsts_login_link, github_login_link = response.github_login_link, google_login_link = response.google_login_link, config = tslib_1.__rest(response, ["vsts_login_link", "github_login_link", "google_login_link"]);
                        authConfig = tslib_1.__assign(tslib_1.__assign({}, config), { vstsLoginLink: vsts_login_link, githubLoginLink: github_login_link, googleLoginLink: google_login_link });
                        this.setState({ authConfig: authConfig });
                        return [3 /*break*/, 4];
                    case 3:
                        e_1 = _a.sent();
                        this.setState({ error: true });
                        return [3 /*break*/, 4];
                    case 4:
                        this.setState({ loading: false });
                        return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    Login.prototype.componentDidMount = function () {
        this.fetchData();
    };
    Object.defineProperty(Login.prototype, "hasAuthProviders", {
        get: function () {
            if (this.state.authConfig === null) {
                return false;
            }
            var _a = this.state.authConfig, githubLoginLink = _a.githubLoginLink, googleLoginLink = _a.googleLoginLink, vstsLoginLink = _a.vstsLoginLink;
            return !!(githubLoginLink || vstsLoginLink || googleLoginLink);
        },
        enumerable: false,
        configurable: true
    });
    Login.prototype.render = function () {
        var _this = this;
        var api = this.props.api;
        var _a = this.state, loading = _a.loading, error = _a.error, activeTab = _a.activeTab, authConfig = _a.authConfig;
        var FormComponent = FORM_COMPONENTS[activeTab];
        var tabs = [
            ['login', locale_1.t('Login')],
            ['sso', locale_1.t('Single Sign-On')],
            ['register', locale_1.t('Register'), !(authConfig === null || authConfig === void 0 ? void 0 : authConfig.canRegister)],
        ];
        var renderTab = function (_a) {
            var _b = tslib_1.__read(_a, 3), key = _b[0], label = _b[1], disabled = _b[2];
            return !disabled && (<li key={key} className={activeTab === key ? 'active' : ''}>
          <a href="#" onClick={function (e) { return _this.handleSetTab(key, e); }}>
            {label}
          </a>
        </li>);
        };
        return (<React.Fragment>
        <Header>
          <Heading>{locale_1.t('Sign in to continue')}</Heading>
          <AuthNavTabs>{tabs.map(renderTab)}</AuthNavTabs>
        </Header>
        {loading && <loadingIndicator_1.default />}
        {error && (<StyledLoadingError message={locale_1.t('Unable to load authentication configuration')} onRetry={this.fetchData}/>)}
        {!loading && authConfig !== null && !error && (<FormWrapper hasAuthProviders={this.hasAuthProviders}>
            <FormComponent {...{ api: api, authConfig: authConfig }}/>
          </FormWrapper>)}
      </React.Fragment>);
    };
    return Login;
}(React.Component));
var StyledLoadingError = styled_1.default(loadingError_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin: ", ";\n"], ["\n  margin: ", ";\n"])), space_1.default(2));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  border-bottom: 1px solid ", ";\n  padding: 20px 40px 0;\n"], ["\n  border-bottom: 1px solid ", ";\n  padding: 20px 40px 0;\n"])), function (p) { return p.theme.border; });
var Heading = styled_1.default('h3')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  font-size: 24px;\n  margin: 0 0 20px 0;\n"], ["\n  font-size: 24px;\n  margin: 0 0 20px 0;\n"])));
var AuthNavTabs = styled_1.default(navTabs_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin: 0;\n"], ["\n  margin: 0;\n"])));
var FormWrapper = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: 35px;\n  width: ", ";\n"], ["\n  padding: 35px;\n  width: ", ";\n"])), function (p) { return (p.hasAuthProviders ? '600px' : '490px'); });
var formFooterClass = "\n  display: grid;\n  grid-template-columns: max-content 1fr;\n  grid-gap: " + space_1.default(1) + ";\n  align-items: center;\n  justify-items: end;\n  border-top: none;\n  margin-bottom: 0;\n  padding: 0;\n";
exports.formFooterClass = formFooterClass;
exports.default = withApi_1.default(Login);
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=login.jsx.map
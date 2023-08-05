Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_keydown_1 = tslib_1.__importDefault(require("react-keydown"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var prop_types_1 = tslib_1.__importDefault(require("prop-types"));
var deployPreview_1 = require("app/actionCreators/deployPreview");
var guides_1 = require("app/actionCreators/guides");
var modal_1 = require("app/actionCreators/modal");
var alertActions_1 = tslib_1.__importDefault(require("app/actions/alertActions"));
var api_1 = require("app/api");
var errorBoundary_1 = tslib_1.__importDefault(require("app/components/errorBoundary"));
var globalModal_1 = tslib_1.__importDefault(require("app/components/globalModal"));
var hookOrDefault_1 = tslib_1.__importDefault(require("app/components/hookOrDefault"));
var indicators_1 = tslib_1.__importDefault(require("app/components/indicators"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var constants_1 = require("app/constants");
var locale_1 = require("app/locale");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var hookStore_1 = tslib_1.__importDefault(require("app/stores/hookStore"));
var organizationsStore_1 = tslib_1.__importDefault(require("app/stores/organizationsStore"));
var organizationStore_1 = tslib_1.__importDefault(require("app/stores/organizationStore"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withConfig_1 = tslib_1.__importDefault(require("app/utils/withConfig"));
var newsletterConsent_1 = tslib_1.__importDefault(require("app/views/newsletterConsent"));
var systemAlerts_1 = tslib_1.__importDefault(require("./systemAlerts"));
var GlobalNotifications = hookOrDefault_1.default({
    hookName: 'component:global-notifications',
    defaultComponent: function () { return null; },
});
function getAlertTypeForProblem(problem) {
    switch (problem.severity) {
        case 'critical':
            return 'error';
        default:
            return 'warning';
    }
}
var App = /** @class */ (function (_super) {
    tslib_1.__extends(App, _super);
    function App() {
        var _a, _b, _c;
        var _this = _super.apply(this, tslib_1.__spreadArray([], tslib_1.__read(arguments))) || this;
        _this.state = {
            loading: false,
            error: false,
            needsUpgrade: ((_a = configStore_1.default.get('user')) === null || _a === void 0 ? void 0 : _a.isSuperuser) && configStore_1.default.get('needsUpgrade'),
            newsletterConsentPrompt: (_c = (_b = configStore_1.default.get('user')) === null || _b === void 0 ? void 0 : _b.flags) === null || _c === void 0 ? void 0 : _c.newsletter_consent_prompt,
        };
        _this.mainContainerRef = react_1.createRef();
        _this.unlistener = organizationStore_1.default.listen(function (state) { return _this.setState({ organization: state.organization }); }, undefined);
        _this.onConfigured = function () { return _this.setState({ needsUpgrade: false }); };
        // this is somewhat hackish
        _this.handleNewsletterConsent = function () {
            return _this.setState({
                newsletterConsentPrompt: false,
            });
        };
        _this.handleGlobalModalClose = function () {
            var _a;
            if (typeof ((_a = _this.mainContainerRef.current) === null || _a === void 0 ? void 0 : _a.focus) === 'function') {
                // Focus the main container to get hotkeys to keep working after modal closes
                _this.mainContainerRef.current.focus();
            }
        };
        return _this;
    }
    App.prototype.getChildContext = function () {
        return {
            location: this.props.location,
        };
    };
    App.prototype.componentDidMount = function () {
        var _this = this;
        this.props.api.request('/organizations/', {
            query: {
                member: '1',
            },
            success: function (data) {
                organizationsStore_1.default.load(data);
                _this.setState({
                    loading: false,
                });
            },
            error: function () {
                _this.setState({
                    loading: false,
                    error: true,
                });
            },
        });
        this.props.api.request('/internal/health/', {
            success: function (data) {
                if (data && data.problems) {
                    data.problems.forEach(function (problem) {
                        alertActions_1.default.addAlert({
                            id: problem.id,
                            message: problem.message,
                            type: getAlertTypeForProblem(problem),
                            url: problem.url,
                        });
                    });
                }
            },
            error: function () { }, // TODO: do something?
        });
        configStore_1.default.get('messages').forEach(function (msg) {
            alertActions_1.default.addAlert({
                message: msg.message,
                type: msg.level,
                neverExpire: true,
            });
        });
        if (constants_1.DEPLOY_PREVIEW_CONFIG) {
            deployPreview_1.displayDeployPreviewAlert();
        }
        else if (constants_1.EXPERIMENTAL_SPA) {
            deployPreview_1.displayExperimentalSpaAlert();
        }
        api_1.initApiClientErrorHandling();
        var user = configStore_1.default.get('user');
        if (user) {
            hookStore_1.default.get('analytics:init-user').map(function (cb) { return cb(user); });
        }
        guides_1.fetchGuides();
    };
    App.prototype.componentDidUpdate = function (prevProps) {
        var config = this.props.config;
        if (!isEqual_1.default(config, prevProps.config)) {
            this.handleConfigStoreChange(config);
        }
    };
    App.prototype.componentWillUnmount = function () {
        var _a;
        organizationsStore_1.default.load([]);
        (_a = this.unlistener) === null || _a === void 0 ? void 0 : _a.call(this);
    };
    App.prototype.handleConfigStoreChange = function (config) {
        var newState = {};
        if (config.needsUpgrade !== undefined) {
            newState.needsUpgrade = config.needsUpgrade;
        }
        if (config.user !== undefined) {
            newState.user = config.user;
        }
        if (Object.keys(newState).length > 0) {
            this.setState(newState);
        }
    };
    App.prototype.openCommandPalette = function (e) {
        modal_1.openCommandPalette();
        e.preventDefault();
        e.stopPropagation();
    };
    App.prototype.toggleDarkMode = function () {
        configStore_1.default.set('theme', configStore_1.default.get('theme') === 'light' ? 'dark' : 'light');
    };
    App.prototype.renderBody = function () {
        var _a = this.state, needsUpgrade = _a.needsUpgrade, newsletterConsentPrompt = _a.newsletterConsentPrompt;
        if (needsUpgrade) {
            var InstallWizard = react_1.lazy(function () { return Promise.resolve().then(function () { return tslib_1.__importStar(require('app/views/admin/installWizard')); }); });
            return (<react_1.Suspense fallback={null}>
          <InstallWizard onConfigured={this.onConfigured}/>;
        </react_1.Suspense>);
        }
        if (newsletterConsentPrompt) {
            return <newsletterConsent_1.default onSubmitSuccess={this.handleNewsletterConsent}/>;
        }
        return this.props.children;
    };
    App.prototype.render = function () {
        if (this.state.loading) {
            return (<loadingIndicator_1.default triangle>
          {locale_1.t('Getting a list of all of your organizations.')}
        </loadingIndicator_1.default>);
        }
        return (<MainContainer tabIndex={-1} ref={this.mainContainerRef}>
        <globalModal_1.default onClose={this.handleGlobalModalClose}/>
        <systemAlerts_1.default className="messages-container"/>
        <GlobalNotifications className="notifications-container messages-container" organization={this.state.organization}/>
        <indicators_1.default className="indicators-container"/>
        <errorBoundary_1.default>{this.renderBody()}</errorBoundary_1.default>
      </MainContainer>);
    };
    App.childContextTypes = {
        location: prop_types_1.default.object,
    };
    tslib_1.__decorate([
        react_keydown_1.default('meta+shift+p', 'meta+k', 'ctrl+shift+p', 'ctrl+k')
    ], App.prototype, "openCommandPalette", null);
    tslib_1.__decorate([
        react_keydown_1.default('meta+shift+l', 'ctrl+shift+l')
    ], App.prototype, "toggleDarkMode", null);
    return App;
}(react_1.Component));
exports.default = withApi_1.default(withConfig_1.default(App));
var MainContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  min-height: 100vh;\n  outline: none;\n  padding-top: ", ";\n"], ["\n  display: flex;\n  flex-direction: column;\n  min-height: 100vh;\n  outline: none;\n  padding-top: ", ";\n"])), function (p) { return (configStore_1.default.get('demoMode') ? p.theme.demo.headerSize : 0); });
var templateObject_1;
//# sourceMappingURL=index.jsx.map
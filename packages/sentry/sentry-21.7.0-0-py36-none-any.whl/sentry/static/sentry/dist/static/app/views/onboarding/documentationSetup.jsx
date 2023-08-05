Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("prism-sentry/index.css");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var projects_1 = require("app/actionCreators/projects");
var alert_1 = tslib_1.__importStar(require("app/components/alert"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var platforms_1 = tslib_1.__importDefault(require("app/data/platforms"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var firstEventFooter_1 = tslib_1.__importDefault(require("./components/firstEventFooter"));
var fullIntroduction_1 = tslib_1.__importDefault(require("./components/fullIntroduction"));
/**
 * The documentation will include the following string should it be missing the
 * verification example, which currently a lot of docs are.
 */
var INCOMPLETE_DOC_FLAG = 'TODO-ADD-VERIFICATION-EXAMPLE';
var DocumentationSetup = /** @class */ (function (_super) {
    tslib_1.__extends(DocumentationSetup, _super);
    function DocumentationSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            platformDocs: null,
            loadedPlatform: null,
            hasError: false,
        };
        _this.fetchData = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, project, organization, platform, platformDocs, error_1;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, project = _a.project, organization = _a.organization, platform = _a.platform;
                        if (!project || !platform) {
                            return [2 /*return*/];
                        }
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, projects_1.loadDocs(api, organization.slug, project.slug, platform)];
                    case 2:
                        platformDocs = _b.sent();
                        this.setState({ platformDocs: platformDocs, loadedPlatform: platform, hasError: false });
                        return [3 /*break*/, 4];
                    case 3:
                        error_1 = _b.sent();
                        this.setState({ hasError: error_1 });
                        throw error_1;
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleFullDocsClick = function () {
            var organization = _this.props.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_view_full_docs', {}, organization);
        };
        return _this;
    }
    DocumentationSetup.prototype.componentDidMount = function () {
        this.fetchData();
    };
    DocumentationSetup.prototype.componentDidUpdate = function (nextProps) {
        if (nextProps.platform !== this.props.platform ||
            nextProps.project !== this.props.project) {
            this.fetchData();
        }
    };
    Object.defineProperty(DocumentationSetup.prototype, "missingExampleWarning", {
        /**
         * TODO(epurkhiser): This can be removed once all documentation has an
         * example for sending the users first event.
         */
        get: function () {
            var _a;
            var _b = this.state, loadedPlatform = _b.loadedPlatform, platformDocs = _b.platformDocs;
            var missingExample = platformDocs && platformDocs.html.includes(INCOMPLETE_DOC_FLAG);
            if (!missingExample) {
                return null;
            }
            return (<alert_1.default type="warning" icon={<icons_1.IconInfo size="md"/>}>
        {locale_1.tct("Looks like this getting started example is still undergoing some\n           work and doesn't include an example for triggering an event quite\n           yet. If you have trouble sending your first event be sure to consult\n           the [docsLink:full documentation] for [platform].", {
                    docsLink: <externalLink_1.default href={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link}/>,
                    platform: (_a = platforms_1.default.find(function (p) { return p.id === loadedPlatform; })) === null || _a === void 0 ? void 0 : _a.name,
                })}
      </alert_1.default>);
        },
        enumerable: false,
        configurable: true
    });
    DocumentationSetup.prototype.render = function () {
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, platform = _b.platform;
        var _c = this.state, loadedPlatform = _c.loadedPlatform, platformDocs = _c.platformDocs, hasError = _c.hasError;
        var currentPlatform = (_a = loadedPlatform !== null && loadedPlatform !== void 0 ? loadedPlatform : platform) !== null && _a !== void 0 ? _a : 'other';
        var docs = platformDocs !== null && (<DocsWrapper key={platformDocs.html}>
        <Content dangerouslySetInnerHTML={{ __html: platformDocs.html }}/>
        {this.missingExampleWarning}

        {project && (<firstEventFooter_1.default project={project} organization={organization} docsLink={platformDocs === null || platformDocs === void 0 ? void 0 : platformDocs.link} docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        var loadingError = (<loadingError_1.default message={locale_1.t('Failed to load documentation for the %s platform.', platform)} onRetry={this.fetchData}/>);
        var testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<React.Fragment>
        <fullIntroduction_1.default currentPlatform={currentPlatform}/>
        {getDynamicText_1.default({
                value: !hasError ? docs : loadingError,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    };
    return DocumentationSetup;
}(React.Component));
var getAlertSelector = function (type) {
    return type === 'muted' ? null : ".alert[level=\"" + type + "\"], .alert-" + type;
};
var mapAlertStyles = function (p, type) {
    return react_1.css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n    ", " {\n      ", ";\n      display: block;\n    }\n  "], ["\n    ", " {\n      ", ";\n      display: block;\n    }\n  "])), getAlertSelector(type), alert_1.alertStyles({ theme: p.theme, type: type }));
};
var Content = styled_1.default(framer_motion_1.motion.div)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  div[data-language] {\n    margin-bottom: ", ";\n  }\n\n  code {\n    font-size: 87.5%;\n    color: ", ";\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"], ["\n  h1,\n  h2,\n  h3,\n  h4,\n  h5,\n  h6,\n  p {\n    margin-bottom: 18px;\n  }\n\n  div[data-language] {\n    margin-bottom: ", ";\n  }\n\n  code {\n    font-size: 87.5%;\n    color: ", ";\n  }\n\n  pre code {\n    color: inherit;\n    font-size: inherit;\n    white-space: pre;\n  }\n\n  h2 {\n    font-size: 1.4em;\n  }\n\n  .alert h5 {\n    font-size: 1em;\n    margin-bottom: 1rem;\n  }\n\n  /**\n   * XXX(epurkhiser): This comes from the doc styles and avoids bottom margin issues in alerts\n   */\n  .content-flush-bottom *:last-child {\n    margin-bottom: 0;\n  }\n\n  ", "\n"])), space_1.default(2), function (p) { return p.theme.pink300; }, function (p) { return Object.keys(p.theme.alert).map(function (type) { return mapAlertStyles(p, type); }); });
var DocsWrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
exports.default = withOrganization_1.default(withApi_1.default(DocumentationSetup));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=documentationSetup.jsx.map
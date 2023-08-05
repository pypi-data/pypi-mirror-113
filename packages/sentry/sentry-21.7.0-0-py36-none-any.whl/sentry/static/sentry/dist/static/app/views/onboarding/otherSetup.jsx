Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
require("prism-sentry/index.css");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var framer_motion_1 = require("framer-motion");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var locale_1 = require("app/locale");
var advancedAnalytics_1 = require("app/utils/advancedAnalytics");
var getDynamicText_1 = tslib_1.__importDefault(require("app/utils/getDynamicText"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var firstEventFooter_1 = tslib_1.__importDefault(require("./components/firstEventFooter"));
var fullIntroduction_1 = tslib_1.__importDefault(require("./components/fullIntroduction"));
var OtherSetup = /** @class */ (function (_super) {
    tslib_1.__extends(OtherSetup, _super);
    function OtherSetup() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFullDocsClick = function () {
            var organization = _this.props.organization;
            advancedAnalytics_1.trackAdvancedAnalyticsEvent('growth.onboarding_view_full_docs', {}, organization);
        };
        return _this;
    }
    OtherSetup.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { keyList: null });
    };
    OtherSetup.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        return [['keyList', "/projects/" + organization.slug + "/" + (project === null || project === void 0 ? void 0 : project.slug) + "/keys/"]];
    };
    OtherSetup.prototype.render = function () {
        var _a = this.props, organization = _a.organization, project = _a.project;
        var keyList = this.state.keyList;
        var currentPlatform = 'other';
        var blurb = (<React.Fragment>
        <p>
          {locale_1.tct("Prepare the SDK for your language following this [docsLink:guide].", {
                docsLink: <externalLink_1.default href="https://develop.sentry.dev/sdk/overview/"/>,
            })}
        </p>

        <p>
          {locale_1.t('Once your SDK is set up, use the following DSN and send your first event!')}
        </p>

        <p>{locale_1.tct('Here is the DSN: [DSN]', { DSN: <b> {keyList === null || keyList === void 0 ? void 0 : keyList[0].dsn.public}</b> })}</p>
      </React.Fragment>);
        var docs = (<DocsWrapper>
        {blurb}
        {project && (<firstEventFooter_1.default project={project} organization={organization} docsLink="https://develop.sentry.dev/sdk" docsOnClick={this.handleFullDocsClick}/>)}
      </DocsWrapper>);
        var testOnlyAlert = (<alert_1.default type="warning">
        Platform documentation is not rendered in for tests in CI
      </alert_1.default>);
        return (<React.Fragment>
        <fullIntroduction_1.default currentPlatform={currentPlatform}/>
        {getDynamicText_1.default({
                value: docs,
                fixed: testOnlyAlert,
            })}
      </React.Fragment>);
    };
    return OtherSetup;
}(asyncComponent_1.default));
var DocsWrapper = styled_1.default(framer_motion_1.motion.div)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject([""], [""])));
DocsWrapper.defaultProps = {
    initial: { opacity: 0, y: 40 },
    animate: { opacity: 1, y: 0 },
    exit: { opacity: 0 },
};
exports.default = withOrganization_1.default(withApi_1.default(OtherSetup));
var templateObject_1;
//# sourceMappingURL=otherSetup.jsx.map
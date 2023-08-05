Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var breadcrumbs_generic_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/breadcrumbs-generic.svg"));
var code_arguments_tags_mirrored_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/code-arguments-tags-mirrored.svg"));
var releases_svg_1 = tslib_1.__importDefault(require("sentry-images/spot/releases.svg"));
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var resourceCard_1 = tslib_1.__importDefault(require("app/components/resourceCard"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var Resources = /** @class */ (function (_super) {
    tslib_1.__extends(Resources, _super);
    function Resources() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Resources.prototype.componentDidMount = function () {
        var organization = this.props.organization;
        analytics_1.trackAnalyticsEvent({
            eventKey: 'orgdash.resources_shown',
            eventName: 'Projects Dashboard: Resources Shown',
            organization_id: organization.id,
        });
    };
    Resources.prototype.render = function () {
        return (<ResourcesWrapper data-test-id="resources">
        <pageHeading_1.default withMargins>{locale_1.t('Resources')}</pageHeading_1.default>
        <ResourceCards>
          <resourceCard_1.default link="https://blog.sentry.io/2018/03/06/the-sentry-workflow" imgUrl={releases_svg_1.default} title={locale_1.t('The Sentry Workflow')}/>
          <resourceCard_1.default link="https://sentry.io/vs/logging/" imgUrl={breadcrumbs_generic_svg_1.default} title={locale_1.t('Sentry vs Logging')}/>
          <resourceCard_1.default link="https://docs.sentry.io/" imgUrl={code_arguments_tags_mirrored_svg_1.default} title={locale_1.t('Docs')}/>
        </ResourceCards>
      </ResourcesWrapper>);
    };
    return Resources;
}(react_1.Component));
exports.default = Resources;
var ResourcesWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-top: 1px solid ", ";\n  padding: 25px 30px 10px 30px;\n"], ["\n  border-top: 1px solid ", ";\n  padding: 25px 30px 10px 30px;\n"])), function (p) { return p.theme.border; });
var ResourceCards = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));\n  }\n"], ["\n  display: grid;\n  grid-template-columns: minmax(100px, 1fr);\n  grid-gap: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));\n  }\n"])), space_1.default(3), function (p) { return p.theme.breakpoints[1]; });
var templateObject_1, templateObject_2;
//# sourceMappingURL=resources.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var globalSelectionLink_1 = tslib_1.__importDefault(require("app/components/globalSelectionLink"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var tokenizeSearch_1 = require("app/utils/tokenizeSearch");
var utils_1 = require("app/views/performance/trends/utils");
var utils_2 = require("app/views/performance/utils");
var styles_2 = require("./styles");
function ProjectQuickLinks(_a) {
    var organization = _a.organization, project = _a.project, location = _a.location;
    function getTrendsLink() {
        var queryString = queryString_1.decodeScalar(location.query.query);
        var conditions = tokenizeSearch_1.tokenizeSearch(queryString || '');
        conditions.setTagValues('tpm()', ['>0.01']);
        conditions.setTagValues('transaction.duration', ['>0', "<" + utils_1.DEFAULT_MAX_DURATION]);
        return {
            pathname: utils_2.getPerformanceTrendsUrl(organization),
            query: {
                project: project === null || project === void 0 ? void 0 : project.id,
                cursor: undefined,
                query: conditions.formatString(),
            },
        };
    }
    var quickLinks = [
        {
            title: locale_1.t('User Feedback'),
            to: {
                pathname: "/organizations/" + organization.slug + "/user-feedback/",
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
        },
        {
            title: locale_1.t('View Transactions'),
            to: {
                pathname: utils_2.getPerformanceLandingUrl(organization),
                query: { project: project === null || project === void 0 ? void 0 : project.id },
            },
            disabled: !organization.features.includes('performance-view'),
        },
        {
            title: locale_1.t('Most Improved/Regressed Transactions'),
            to: getTrendsLink(),
            disabled: !organization.features.includes('performance-view'),
        },
    ];
    return (<styles_2.SidebarSection>
      <styles_1.SectionHeading>{locale_1.t('Quick Links')}</styles_1.SectionHeading>
      {quickLinks
            // push disabled links to the bottom
            .sort(function (link1, link2) { return Number(!!link1.disabled) - Number(!!link2.disabled); })
            .map(function (_a) {
            var title = _a.title, to = _a.to, disabled = _a.disabled;
            return (<div key={title}>
            <tooltip_1.default title={locale_1.t("You don't have access to this feature")} disabled={!disabled}>
              <QuickLink to={to} disabled={disabled}>
                <icons_1.IconLink />
                <QuickLinkText>{title}</QuickLinkText>
              </QuickLink>
            </tooltip_1.default>
          </div>);
        })}
    </styles_2.SidebarSection>);
}
var QuickLink = styled_1.default(function (p) {
    return p.disabled ? (<span className={p.className}>{p.children}</span>) : (<globalSelectionLink_1.default {...p}/>);
})(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n  display: grid;\n  align-items: center;\n  gap: ", ";\n  grid-template-columns: auto 1fr;\n\n  ", "\n"], ["\n  margin-bottom: ", ";\n  display: grid;\n  align-items: center;\n  gap: ", ";\n  grid-template-columns: auto 1fr;\n\n  ", "\n"])), space_1.default(1), space_1.default(1), function (p) {
    return p.disabled &&
        "\n    color: " + p.theme.gray200 + ";\n    cursor: not-allowed;\n  ";
});
var QuickLinkText = styled_1.default('span')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  font-size: ", ";\n  ", "\n"], ["\n  font-size: ", ";\n  ", "\n"])), function (p) { return p.theme.fontSizeMedium; }, overflowEllipsis_1.default);
exports.default = ProjectQuickLinks;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectQuickLinks.jsx.map
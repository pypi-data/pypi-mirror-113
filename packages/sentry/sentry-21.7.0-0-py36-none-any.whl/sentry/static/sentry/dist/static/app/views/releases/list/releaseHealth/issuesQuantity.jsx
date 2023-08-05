Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var count_1 = tslib_1.__importDefault(require("app/components/count"));
var link_1 = tslib_1.__importDefault(require("app/components/links/link"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("../../utils");
var IssuesQuantity = function (_a) {
    var orgSlug = _a.orgSlug, newGroups = _a.newGroups, projectId = _a.projectId, releaseVersion = _a.releaseVersion, _b = _a.isCompact, isCompact = _b === void 0 ? false : _b;
    return (<tooltip_1.default title={locale_1.t('Open in Issues')}>
    <link_1.default to={utils_1.getReleaseNewIssuesUrl(orgSlug, projectId, releaseVersion)}>
      {isCompact ? (<Issues>
          <StyledCount value={newGroups}/>
          <span>{locale_1.tn('issue', 'issues', newGroups)}</span>
        </Issues>) : (<count_1.default value={newGroups}/>)}
    </link_1.default>
  </tooltip_1.default>);
};
exports.default = IssuesQuantity;
var Issues = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content;\n  justify-content: flex-end;\n  align-items: center;\n  text-align: end;\n"], ["\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: auto max-content;\n  justify-content: flex-end;\n  align-items: center;\n  text-align: end;\n"])), space_1.default(0.5));
// overflowEllipsis is useful if the count's value is over 1000000000
var StyledCount = styled_1.default(count_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n"], ["\n  ", "\n"])), overflowEllipsis_1.default);
var templateObject_1, templateObject_2;
//# sourceMappingURL=issuesQuantity.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var projectApdexScoreCard_1 = tslib_1.__importDefault(require("./projectApdexScoreCard"));
var projectStabilityScoreCard_1 = tslib_1.__importDefault(require("./projectStabilityScoreCard"));
var projectVelocityScoreCard_1 = tslib_1.__importDefault(require("./projectVelocityScoreCard"));
function ProjectScoreCards(_a) {
    var organization = _a.organization, selection = _a.selection, isProjectStabilized = _a.isProjectStabilized, hasSessions = _a.hasSessions, hasTransactions = _a.hasTransactions, query = _a.query;
    return (<CardWrapper>
      <projectStabilityScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasSessions={hasSessions} query={query}/>

      <projectVelocityScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} query={query}/>

      <projectApdexScoreCard_1.default organization={organization} selection={selection} isProjectStabilized={isProjectStabilized} hasTransactions={hasTransactions} query={query}/>
    </CardWrapper>);
}
var CardWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-column-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"], ["\n  display: grid;\n  grid-template-columns: repeat(3, minmax(0, 1fr));\n  grid-column-gap: ", ";\n\n  @media (max-width: ", ") {\n    grid-template-columns: 1fr;\n    grid-template-rows: repeat(3, 1fr);\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
exports.default = ProjectScoreCards;
var templateObject_1;
//# sourceMappingURL=projectScoreCards.jsx.map
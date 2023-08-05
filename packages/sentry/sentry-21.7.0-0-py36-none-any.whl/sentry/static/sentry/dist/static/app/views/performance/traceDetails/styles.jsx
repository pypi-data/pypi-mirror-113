Object.defineProperty(exports, "__esModule", { value: true });
exports.Tags = exports.StyledProjectBadge = exports.StyledPanel = exports.TraceViewContainer = exports.TraceDetailBody = exports.TraceDetailHeader = exports.TraceViewHeaderContainer = exports.StyledSearchBar = exports.SearchContainer = exports.TransactionDetailsContainer = exports.TransactionDetails = exports.Row = void 0;
var tslib_1 = require("tslib");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var eventTagsPill_1 = tslib_1.__importDefault(require("app/components/events/eventTags/eventTagsPill"));
var header_1 = require("app/components/events/interfaces/spans/header");
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var panels_1 = require("app/components/panels");
var pills_1 = tslib_1.__importDefault(require("app/components/pills"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var utils_1 = require("app/utils");
var queryString_1 = require("app/utils/queryString");
var utils_2 = require("app/views/performance/transactionSummary/utils");
var spanDetail_1 = require("app/components/events/interfaces/spans/spanDetail");
Object.defineProperty(exports, "Row", { enumerable: true, get: function () { return spanDetail_1.Row; } });
Object.defineProperty(exports, "TransactionDetails", { enumerable: true, get: function () { return spanDetail_1.SpanDetails; } });
Object.defineProperty(exports, "TransactionDetailsContainer", { enumerable: true, get: function () { return spanDetail_1.SpanDetailContainer; } });
exports.SearchContainer = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  width: 100%;\n"], ["\n  display: flex;\n  width: 100%;\n"])));
exports.StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
exports.TraceViewHeaderContainer = styled_1.default(header_1.SecondaryHeader)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  position: static;\n  top: auto;\n  border-top: none;\n  border-bottom: 1px solid ", ";\n"], ["\n  position: static;\n  top: auto;\n  border-top: none;\n  border-bottom: 1px solid ", ";\n"])), function (p) { return p.theme.border; });
exports.TraceDetailHeader = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(250px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: 1fr;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: minmax(250px, 1fr) minmax(160px, 1fr) 6fr;\n    grid-row-gap: 0;\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[1]; });
exports.TraceDetailBody = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-top: ", ";\n"], ["\n  margin-top: ", ";\n"])), space_1.default(2));
exports.TraceViewContainer = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"], ["\n  overflow-x: hidden;\n  border-bottom-left-radius: 3px;\n  border-bottom-right-radius: 3px;\n"])));
exports.StyledPanel = styled_1.default(panels_1.Panel)(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  overflow: hidden;\n"], ["\n  overflow: hidden;\n"])));
exports.StyledProjectBadge = styled_1.default(projectBadge_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  margin-right: ", ";\n"], ["\n  margin-right: ", ";\n"])), space_1.default(0.75));
var StyledPills = styled_1.default(pills_1.default)(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  padding-top: ", ";\n"], ["\n  padding-top: ", ";\n"])), space_1.default(1.5));
function Tags(_a) {
    var location = _a.location, organization = _a.organization, transaction = _a.transaction;
    var tags = transaction.tags;
    if (!tags || tags.length <= 0) {
        return null;
    }
    var orgSlug = organization.slug;
    var releasesPath = "/organizations/" + orgSlug + "/releases/";
    return (<tr>
      <td className="key">Tags</td>
      <td className="value">
        <StyledPills>
          {tags.map(function (tag, index) {
            var _a = utils_2.transactionSummaryRouteWithQuery({
                orgSlug: orgSlug,
                transaction: transaction.transaction,
                projectID: String(transaction.project_id),
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { query: queryString_1.appendTagCondition(location.query.query, tag.key, tag.value) }),
            }), streamPath = _a.pathname, query = _a.query;
            return (<eventTagsPill_1.default key={!utils_1.defined(tag.key) ? "tag-pill-" + index : tag.key} tag={tag} projectId={transaction.project_slug} organization={organization} query={query} streamPath={streamPath} releasesPath={releasesPath} hasQueryFeature={false}/>);
        })}
        </StyledPills>
      </td>
    </tr>);
}
exports.Tags = Tags;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=styles.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var guideAnchor_1 = tslib_1.__importDefault(require("app/components/assistant/guideAnchor"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var displayOptions_1 = tslib_1.__importDefault(require("./displayOptions"));
var searchBar_1 = tslib_1.__importDefault(require("./searchBar"));
var sortOptions_1 = tslib_1.__importDefault(require("./sortOptions"));
var IssueListFilters = /** @class */ (function (_super) {
    tslib_1.__extends(IssueListFilters, _super);
    function IssueListFilters() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    IssueListFilters.prototype.render = function () {
        var _a = this.props, organization = _a.organization, savedSearch = _a.savedSearch, query = _a.query, isSearchDisabled = _a.isSearchDisabled, sort = _a.sort, display = _a.display, hasSessions = _a.hasSessions, selectedProjects = _a.selectedProjects, onSidebarToggle = _a.onSidebarToggle, onSearch = _a.onSearch, onSortChange = _a.onSortChange, onDisplayChange = _a.onDisplayChange, tagValueLoader = _a.tagValueLoader, tags = _a.tags;
        var isAssignedQuery = /\bassigned:/.test(query);
        return (<organization_1.PageHeader>
        <SearchContainer>
          <react_1.ClassNames>
            {function (_a) {
                var css = _a.css;
                return (<guideAnchor_1.default target="assigned_or_suggested_query" disabled={!isAssignedQuery} containerClassName={css(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n                  width: 100%;\n                "], ["\n                  width: 100%;\n                "])))}>
                <searchBar_1.default organization={organization} query={query || ''} sort={sort} onSearch={onSearch} disabled={isSearchDisabled} excludeEnvironment supportedTags={tags} tagValueLoader={tagValueLoader} savedSearch={savedSearch} onSidebarToggle={onSidebarToggle}/>
              </guideAnchor_1.default>);
            }}
          </react_1.ClassNames>
          <buttonBar_1.default gap={1}>
            <feature_1.default features={['issue-percent-display']} organization={organization}>
              <displayOptions_1.default onDisplayChange={onDisplayChange} display={display} hasSessions={hasSessions} hasMultipleProjectsSelected={selectedProjects.length !== 1 || selectedProjects[0] === -1}/>
            </feature_1.default>
            <sortOptions_1.default sort={sort} query={query} onSelect={onSortChange}/>
          </buttonBar_1.default>
        </SearchContainer>
      </organization_1.PageHeader>);
    };
    return IssueListFilters;
}(React.Component));
var SearchContainer = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n  width: 100%;\n"], ["\n  display: grid;\n  grid-template-columns: 1fr max-content;\n  grid-gap: ", ";\n  align-items: start;\n  width: 100%;\n"])), space_1.default(1));
exports.default = IssueListFilters;
var templateObject_1, templateObject_2;
//# sourceMappingURL=filters.jsx.map
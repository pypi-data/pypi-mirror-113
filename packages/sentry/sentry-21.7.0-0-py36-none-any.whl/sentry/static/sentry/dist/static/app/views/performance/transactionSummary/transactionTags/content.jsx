Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var styles_1 = require("app/components/charts/styles");
var searchBar_1 = tslib_1.__importDefault(require("app/components/events/searchBar"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var radio_1 = tslib_1.__importDefault(require("app/components/radio"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var segmentExplorerQuery_1 = tslib_1.__importDefault(require("app/utils/performance/segmentExplorer/segmentExplorerQuery"));
var queryString_1 = require("app/utils/queryString");
var utils_1 = require("app/views/performance/transactionSummary/utils");
var utils_2 = require("../../landing/utils");
var filter_1 = require("../filter");
var header_1 = tslib_1.__importStar(require("../header"));
var tagExplorer_1 = require("../tagExplorer");
var tagsDisplay_1 = tslib_1.__importDefault(require("./tagsDisplay"));
var utils_3 = require("./utils");
var TagsPageContent = function (props) {
    var eventView = props.eventView, location = props.location, organization = props.organization, projects = props.projects, transactionName = props.transactionName;
    var handleIncompatibleQuery = function () { };
    var aggregateColumn = tagExplorer_1.getTransactionField(filter_1.SpanOperationBreakdownFilter.None, projects, eventView);
    return (<react_1.Fragment>
      <header_1.default eventView={eventView} location={location} organization={organization} projects={projects} transactionName={transactionName} currentTab={header_1.Tab.Tags} hasWebVitals={utils_2.getCurrentLandingDisplay(location, projects, eventView).field ===
            utils_2.LandingDisplayField.FRONTEND_PAGELOAD} handleIncompatibleQuery={handleIncompatibleQuery}/>

      <segmentExplorerQuery_1.default eventView={eventView} orgSlug={organization.slug} location={location} aggregateColumn={aggregateColumn} limit={20} sort="-sumdelta" allTagKeys>
        {function (_a) {
            var isLoading = _a.isLoading, tableData = _a.tableData;
            return <InnerContent {...props} isLoading={isLoading} tableData={tableData}/>;
        }}
      </segmentExplorerQuery_1.default>
    </react_1.Fragment>);
};
function getTagKeyOptions(tableData) {
    var suspectTags = [];
    var otherTags = [];
    tableData.data.forEach(function (row) {
        var tagArray = row.comparison > 1 ? suspectTags : otherTags;
        tagArray.push(row.tags_key);
    });
    return {
        suspectTags: suspectTags,
        otherTags: otherTags,
    };
}
var InnerContent = function (props) {
    var _eventView = props.eventView, location = props.location, organization = props.organization, tableData = props.tableData, isLoading = props.isLoading;
    var eventView = _eventView.clone();
    var tagOptions = tableData ? getTagKeyOptions(tableData) : null;
    var suspectTags = tagOptions ? tagOptions.suspectTags : [];
    var otherTags = tagOptions ? tagOptions.otherTags : [];
    var decodedTagKey = utils_3.decodeSelectedTagKey(location);
    var allTags = tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(suspectTags)), tslib_1.__read(otherTags));
    var decodedTagFromOptions = decodedTagKey
        ? allTags.find(function (tag) { return tag === decodedTagKey; })
        : undefined;
    var defaultTag = allTags.length ? allTags[0] : undefined;
    var initialTag = decodedTagFromOptions !== null && decodedTagFromOptions !== void 0 ? decodedTagFromOptions : defaultTag;
    var _a = tslib_1.__read(react_1.useState(initialTag), 2), tagSelected = _a[0], _changeTagSelected = _a[1];
    var changeTagSelected = function (tagKey) {
        var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { tagKey: tagKey }));
        react_router_1.browserHistory.replace({
            pathname: location.pathname,
            query: queryParams,
        });
        _changeTagSelected(tagKey);
    };
    react_1.useEffect(function () {
        if (initialTag) {
            changeTagSelected(initialTag);
        }
    }, [initialTag]);
    var handleSearch = function (query) {
        var queryParams = getParams_1.getParams(tslib_1.__assign(tslib_1.__assign({}, (location.query || {})), { query: query }));
        react_router_1.browserHistory.push({
            pathname: location.pathname,
            query: queryParams,
        });
    };
    var changeTag = function (tag) {
        return changeTagSelected(tag);
    };
    if (tagSelected) {
        eventView.additionalConditions.setTagValues('has', [tagSelected]);
    }
    var query = queryString_1.decodeScalar(location.query.query, '');
    return (<ReversedLayoutBody>
      <TagsSideBar suspectTags={suspectTags} otherTags={otherTags} tagSelected={tagSelected} changeTag={changeTag} isLoading={isLoading}/>
      <StyledMain>
        <StyledActions>
          <StyledSearchBar organization={organization} projectIds={eventView.project} query={query} fields={eventView.fields} onSearch={handleSearch}/>
        </StyledActions>
        <tagsDisplay_1.default {...props} tagKey={tagSelected}/>
      </StyledMain>
    </ReversedLayoutBody>);
};
var TagsSideBar = function (props) {
    var suspectTags = props.suspectTags, otherTags = props.otherTags, changeTag = props.changeTag, tagSelected = props.tagSelected, isLoading = props.isLoading;
    return (<StyledSide>
      <StyledSectionHeading>
        {locale_1.t('Suspect Tags')}
        <questionTooltip_1.default position="top" title={locale_1.t('Suspect tags are tags that often correspond to slower transaction')} size="sm"/>
      </StyledSectionHeading>
      {isLoading ? (<Center>
          <loadingIndicator_1.default mini/>
        </Center>) : suspectTags.length ? (suspectTags.map(function (tag) { return (<RadioLabel key={tag}>
            <radio_1.default aria-label={tag} checked={tagSelected === tag} onChange={function () { return changeTag(tag); }}/>
            <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
          </RadioLabel>); })) : (<div>{locale_1.t('No tags detected.')}</div>)}

      <utils_1.SidebarSpacer />
      <StyledSectionHeading>
        {locale_1.t('Other Tags')}
        <questionTooltip_1.default position="top" title={locale_1.t('Other common tags for this transaction')} size="sm"/>
      </StyledSectionHeading>

      {isLoading ? (<Center>
          <loadingIndicator_1.default mini/>
        </Center>) : otherTags.length ? (otherTags.map(function (tag) { return (<RadioLabel key={tag}>
            <radio_1.default aria-label={tag} checked={tagSelected === tag} onChange={function () { return changeTag(tag); }}/>
            <SidebarTagValue className="truncate">{tag}</SidebarTagValue>
          </RadioLabel>); })) : (<div>{locale_1.t('No tags detected.')}</div>)}
    </StyledSide>);
};
var Center = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"], ["\n  display: flex;\n  align-items: center;\n  justify-content: center;\n"])));
var RadioLabel = styled_1.default('label')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  cursor: pointer;\n  margin-bottom: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"], ["\n  cursor: pointer;\n  margin-bottom: ", ";\n  font-weight: normal;\n  display: grid;\n  grid-auto-flow: column;\n  grid-auto-columns: max-content 1fr;\n  align-items: center;\n  grid-gap: ", ";\n"])), space_1.default(1), space_1.default(1));
var SidebarTagValue = styled_1.default('span')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  width: 100%;\n"], ["\n  width: 100%;\n"])));
var StyledSectionHeading = styled_1.default(styles_1.SectionHeading)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(2));
// TODO(k-fish): Adjust thirds layout to allow for this instead.
var ReversedLayoutBody = styled_1.default('div')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: auto 66%;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 225px minmax(100px, auto);\n  }\n"], ["\n  padding: ", ";\n  margin: 0;\n  background-color: ", ";\n  flex-grow: 1;\n\n  @media (min-width: ", ") {\n    padding: ", " ", ";\n  }\n\n  @media (min-width: ", ") {\n    display: grid;\n    grid-template-columns: auto 66%;\n    align-content: start;\n    grid-gap: ", ";\n  }\n\n  @media (min-width: ", ") {\n    grid-template-columns: 225px minmax(100px, auto);\n  }\n"])), space_1.default(2), function (p) { return p.theme.background; }, function (p) { return p.theme.breakpoints[0]; }, space_1.default(3), space_1.default(4), function (p) { return p.theme.breakpoints[1]; }, space_1.default(3), function (p) { return p.theme.breakpoints[2]; });
var StyledSide = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  grid-column: 1/2;\n"], ["\n  grid-column: 1/2;\n"])));
var StyledMain = styled_1.default('div')(templateObject_7 || (templateObject_7 = tslib_1.__makeTemplateObject(["\n  grid-column: 2/4;\n  max-width: 100%;\n"], ["\n  grid-column: 2/4;\n  max-width: 100%;\n"])));
var StyledSearchBar = styled_1.default(searchBar_1.default)(templateObject_8 || (templateObject_8 = tslib_1.__makeTemplateObject(["\n  flex-grow: 1;\n"], ["\n  flex-grow: 1;\n"])));
var StyledActions = styled_1.default('div')(templateObject_9 || (templateObject_9 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1));
exports.default = TagsPageContent;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6, templateObject_7, templateObject_8, templateObject_9;
//# sourceMappingURL=content.jsx.map
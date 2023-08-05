Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var panelTable_1 = tslib_1.__importDefault(require("app/components/panels/panelTable"));
var questionTooltip_1 = tslib_1.__importDefault(require("app/components/questionTooltip"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var debugImage_1 = require("app/types/debugImage");
var utils_1 = require("app/utils");
var searchBarAction_1 = tslib_1.__importDefault(require("../../searchBarAction"));
var searchBarActionFilter_1 = tslib_1.__importDefault(require("../../searchBarAction/searchBarActionFilter"));
var status_1 = tslib_1.__importDefault(require("./candidate/status"));
var candidate_1 = tslib_1.__importDefault(require("./candidate"));
var utils_2 = require("./utils");
var filterOptionCategories = {
    status: locale_1.t('Status'),
    source: locale_1.t('Source'),
};
var Candidates = /** @class */ (function (_super) {
    tslib_1.__extends(Candidates, _super);
    function Candidates() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            searchTerm: '',
            filterOptions: {},
            filteredCandidatesBySearch: [],
            filteredCandidatesByFilter: [],
        };
        _this.doSearch = debounce_1.default(_this.filterCandidatesBySearch, 300);
        _this.handleChangeSearchTerm = function (searchTerm) {
            if (searchTerm === void 0) { searchTerm = ''; }
            _this.setState({ searchTerm: searchTerm });
        };
        _this.handleChangeFilter = function (filterOptions) {
            var filteredCandidatesBySearch = _this.state.filteredCandidatesBySearch;
            var filteredCandidatesByFilter = _this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
            _this.setState({ filterOptions: filterOptions, filteredCandidatesByFilter: filteredCandidatesByFilter });
        };
        _this.handleResetFilter = function () {
            var filterOptions = _this.state.filterOptions;
            _this.setState({
                filterOptions: Object.keys(filterOptions).reduce(function (accumulator, currentValue) {
                    accumulator[currentValue] = filterOptions[currentValue].map(function (filterOption) { return (tslib_1.__assign(tslib_1.__assign({}, filterOption), { isChecked: false })); });
                    return accumulator;
                }, {}),
            }, _this.filterCandidatesBySearch);
        };
        _this.handleResetSearchBar = function () {
            var candidates = _this.props.candidates;
            _this.setState({
                searchTerm: '',
                filteredCandidatesByFilter: candidates,
                filteredCandidatesBySearch: candidates,
            });
        };
        return _this;
    }
    Candidates.prototype.componentDidMount = function () {
        this.getFilters();
    };
    Candidates.prototype.componentDidUpdate = function (prevProps, prevState) {
        if (!isEqual_1.default(prevProps.candidates, this.props.candidates)) {
            this.getFilters();
            return;
        }
        if (prevState.searchTerm !== this.state.searchTerm) {
            this.doSearch();
        }
    };
    Candidates.prototype.filterCandidatesBySearch = function () {
        var _a = this.state, searchTerm = _a.searchTerm, filterOptions = _a.filterOptions;
        var candidates = this.props.candidates;
        if (!searchTerm.trim()) {
            var filteredCandidatesByFilter_1 = this.getFilteredCandidatedByFilter(candidates, filterOptions);
            this.setState({
                filteredCandidatesBySearch: candidates,
                filteredCandidatesByFilter: filteredCandidatesByFilter_1,
            });
            return;
        }
        // Slightly hacky, but it works
        // the string is being `stringfy`d here in order to match exactly the same `stringfy`d string of the loop
        var searchFor = JSON.stringify(searchTerm)
            // it replaces double backslash generate by JSON.stringfy with single backslash
            .replace(/((^")|("$))/g, '')
            .toLocaleLowerCase();
        var filteredCandidatesBySearch = candidates.filter(function (obj) {
            return Object.keys(pick_1.default(obj, ['source_name', 'location'])).some(function (key) {
                var info = obj[key];
                if (key === 'location' && typeof Number(info) === 'number') {
                    return false;
                }
                if (!utils_1.defined(info) || !String(info).trim()) {
                    return false;
                }
                return JSON.stringify(info)
                    .replace(/((^")|("$))/g, '')
                    .toLocaleLowerCase()
                    .trim()
                    .includes(searchFor);
            });
        });
        var filteredCandidatesByFilter = this.getFilteredCandidatedByFilter(filteredCandidatesBySearch, filterOptions);
        this.setState({
            filteredCandidatesBySearch: filteredCandidatesBySearch,
            filteredCandidatesByFilter: filteredCandidatesByFilter,
        });
    };
    Candidates.prototype.getFilters = function () {
        var candidates = tslib_1.__spreadArray([], tslib_1.__read(this.props.candidates));
        var filterOptions = this.getFilterOptions(candidates);
        this.setState({
            filterOptions: filterOptions,
            filteredCandidatesBySearch: candidates,
            filteredCandidatesByFilter: this.getFilteredCandidatedByFilter(candidates, filterOptions),
        });
    };
    Candidates.prototype.getFilterOptions = function (candidates) {
        var imageStatus = this.props.imageStatus;
        var filterOptions = {};
        var candidateStatus = tslib_1.__spreadArray([], tslib_1.__read(new Set(candidates.map(function (candidate) { return candidate.download.status; }))));
        if (candidateStatus.length > 1) {
            filterOptions[filterOptionCategories.status] = candidateStatus.map(function (status) { return ({
                id: status,
                symbol: <status_1.default status={status}/>,
                isChecked: status !== debugImage_1.CandidateDownloadStatus.NOT_FOUND ||
                    imageStatus === debugImage_1.ImageStatus.MISSING,
            }); });
        }
        var candidateSources = tslib_1.__spreadArray([], tslib_1.__read(new Set(candidates.map(function (candidate) { var _a; return (_a = candidate.source_name) !== null && _a !== void 0 ? _a : locale_1.t('Unknown'); }))));
        if (candidateSources.length > 1) {
            filterOptions[filterOptionCategories.source] = candidateSources.map(function (sourceName) { return ({
                id: sourceName,
                symbol: sourceName,
                isChecked: false,
            }); });
        }
        return filterOptions;
    };
    Candidates.prototype.getFilteredCandidatedByFilter = function (candidates, filterOptions) {
        var _a, _b;
        var checkedStatusOptions = new Set((_a = filterOptions[filterOptionCategories.status]) === null || _a === void 0 ? void 0 : _a.filter(function (filterOption) { return filterOption.isChecked; }).map(function (option) { return option.id; }));
        var checkedSourceOptions = new Set((_b = filterOptions[filterOptionCategories.source]) === null || _b === void 0 ? void 0 : _b.filter(function (filterOption) { return filterOption.isChecked; }).map(function (option) { return option.id; }));
        if (checkedStatusOptions.size === 0 && checkedSourceOptions.size === 0) {
            return candidates;
        }
        if (checkedStatusOptions.size > 0) {
            var filteredByStatus = candidates.filter(function (candidate) {
                return checkedStatusOptions.has(candidate.download.status);
            });
            if (checkedSourceOptions.size === 0) {
                return filteredByStatus;
            }
            return filteredByStatus.filter(function (candidate) { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
        }
        return candidates.filter(function (candidate) { var _a; return checkedSourceOptions.has((_a = candidate === null || candidate === void 0 ? void 0 : candidate.source_name) !== null && _a !== void 0 ? _a : ''); });
    };
    Candidates.prototype.getEmptyMessage = function () {
        var _a = this.state, searchTerm = _a.searchTerm, images = _a.filteredCandidatesByFilter, filterOptions = _a.filterOptions;
        if (!!images.length) {
            return {};
        }
        var hasActiveFilter = Object.values(filterOptions)
            .flatMap(function (filterOption) { return filterOption; })
            .find(function (filterOption) { return filterOption.isChecked; });
        if (searchTerm || hasActiveFilter) {
            return {
                emptyMessage: locale_1.t('Sorry, no debug files match your search query'),
                emptyAction: hasActiveFilter ? (<button_1.default onClick={this.handleResetFilter} priority="primary">
            {locale_1.t('Reset filter')}
          </button_1.default>) : (<button_1.default onClick={this.handleResetSearchBar} priority="primary">
            {locale_1.t('Clear search bar')}
          </button_1.default>),
            };
        }
        return {
            emptyMessage: locale_1.t('There are no debug files to be displayed'),
        };
    };
    Candidates.prototype.render = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, baseUrl = _a.baseUrl, builtinSymbolSources = _a.builtinSymbolSources, onDelete = _a.onDelete, isLoading = _a.isLoading, candidates = _a.candidates, eventDateReceived = _a.eventDateReceived, hasReprocessWarning = _a.hasReprocessWarning;
        var _b = this.state, searchTerm = _b.searchTerm, filterOptions = _b.filterOptions, filteredCandidatesByFilter = _b.filteredCandidatesByFilter;
        var haveCandidatesOkOrDeletedDebugFile = candidates.some(function (candidate) {
            return (candidate.download.status === debugImage_1.CandidateDownloadStatus.OK &&
                candidate.source === utils_2.INTERNAL_SOURCE) ||
                candidate.download.status === debugImage_1.CandidateDownloadStatus.DELETED;
        });
        var haveCandidatesAtLeastOneAction = haveCandidatesOkOrDeletedDebugFile || hasReprocessWarning;
        return (<Wrapper>
        <Header>
          <Title>
            {locale_1.t('Debug File Candidates')}
            <questionTooltip_1.default title={locale_1.tct('These are the Debug Information Files (DIFs) corresponding to this image which have been looked up on [docLink:symbol servers] during the processing of the stacktrace.', {
                docLink: (<externalLink_1.default href="https://docs.sentry.io/platforms/native/data-management/debug-files/symbol-servers/"/>),
            })} size="xs" position="top" isHoverable/>
          </Title>
          {!!candidates.length && (<StyledSearchBarAction query={searchTerm} onChange={function (value) { return _this.handleChangeSearchTerm(value); }} placeholder={locale_1.t('Search debug file candidates')} filter={<searchBarActionFilter_1.default options={filterOptions} onChange={this.handleChangeFilter}/>}/>)}
        </Header>
        <StyledPanelTable headers={haveCandidatesAtLeastOneAction
                ? [locale_1.t('Status'), locale_1.t('Information'), '']
                : [locale_1.t('Status'), locale_1.t('Information')]} isEmpty={!filteredCandidatesByFilter.length} isLoading={isLoading} {...this.getEmptyMessage()}>
          {filteredCandidatesByFilter.map(function (candidate, index) { return (<candidate_1.default key={index} candidate={candidate} builtinSymbolSources={builtinSymbolSources} organization={organization} baseUrl={baseUrl} projectId={projectId} eventDateReceived={eventDateReceived} hasReprocessWarning={hasReprocessWarning} haveCandidatesAtLeastOneAction={haveCandidatesAtLeastOneAction} onDelete={onDelete}/>); })}
        </StyledPanelTable>
      </Wrapper>);
    };
    return Candidates;
}(React.Component));
exports.default = Candidates;
var Wrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n"], ["\n  display: grid;\n"])));
var Header = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-wrap: wrap;\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-wrap: wrap;\n    flex-direction: row;\n  }\n"])), function (props) { return props.theme.breakpoints[0]; });
var Title = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  padding-right: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n  height: 32px;\n  flex: 1;\n\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"], ["\n  padding-right: ", ";\n  display: grid;\n  grid-gap: ", ";\n  grid-template-columns: repeat(2, max-content);\n  align-items: center;\n  font-weight: 600;\n  color: ", ";\n  height: 32px;\n  flex: 1;\n\n  @media (min-width: ", ") {\n    margin-bottom: ", ";\n  }\n"])), space_1.default(4), space_1.default(0.5), function (p) { return p.theme.gray400; }, function (props) { return props.theme.breakpoints[0]; }, space_1.default(1));
var StyledPanelTable = styled_1.default(panelTable_1.default)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: ", ";\n\n  height: 100%;\n\n  @media (min-width: ", ") {\n    overflow: visible;\n  }\n"], ["\n  grid-template-columns: ", ";\n\n  height: 100%;\n\n  @media (min-width: ", ") {\n    overflow: visible;\n  }\n"])), function (p) {
    return p.headers.length === 3 ? 'max-content 1fr max-content' : 'max-content 1fr';
}, function (props) { return props.theme.breakpoints[4]; });
var StyledSearchBarAction = styled_1.default(searchBarAction_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  margin-bottom: ", ";\n"], ["\n  margin-bottom: ", ";\n"])), space_1.default(1.5));
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=candidates.jsx.map
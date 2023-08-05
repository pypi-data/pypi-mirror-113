Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var debounce_1 = tslib_1.__importDefault(require("lodash/debounce"));
var globalSelection_1 = require("app/actionCreators/globalSelection");
var backToIssues_1 = tslib_1.__importDefault(require("app/components/organizations/backToIssues"));
var headerItemPosition_1 = tslib_1.__importDefault(require("app/components/organizations/headerItemPosition"));
var headerSeparator_1 = tslib_1.__importDefault(require("app/components/organizations/headerSeparator"));
var multipleEnvironmentSelector_1 = tslib_1.__importDefault(require("app/components/organizations/multipleEnvironmentSelector"));
var multipleProjectSelector_1 = tslib_1.__importDefault(require("app/components/organizations/multipleProjectSelector"));
var timeRangeSelector_1 = tslib_1.__importDefault(require("app/components/organizations/timeRangeSelector"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var constants_1 = require("app/constants");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var callIfFunction_1 = require("app/utils/callIfFunction");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var header_1 = tslib_1.__importDefault(require("./header"));
var PROJECTS_PER_PAGE = 50;
var defaultProps = {
    /**
     * Display Environment selector?
     */
    showEnvironmentSelector: true,
    /**
     * Display date selector?
     */
    showDateSelector: true,
    /**
     * Reset these URL params when we fire actions
     * (custom routing only)
     */
    resetParamsOnChange: [],
    /**
     * Remove ability to select multiple projects even if organization has feature 'global-views'
     */
    disableMultipleProjectSelection: false,
};
var GlobalSelectionHeader = /** @class */ (function (_super) {
    tslib_1.__extends(GlobalSelectionHeader, _super);
    function GlobalSelectionHeader() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            projects: null,
            environments: null,
            searchQuery: '',
        };
        _this.hasMultipleProjectSelection = function () {
            return new Set(_this.props.organization.features).has('global-views');
        };
        // Returns an options object for `update*` actions
        _this.getUpdateOptions = function () { return ({
            save: true,
            resetParams: _this.props.resetParamsOnChange,
        }); };
        _this.handleChangeProjects = function (projects) {
            _this.setState({
                projects: projects,
            });
            callIfFunction_1.callIfFunction(_this.props.onChangeProjects, projects);
        };
        _this.handleChangeEnvironments = function (environments) {
            _this.setState({
                environments: environments,
            });
            callIfFunction_1.callIfFunction(_this.props.onChangeEnvironments, environments);
        };
        _this.handleChangeTime = function (_a) {
            var start = _a.start, end = _a.end, period = _a.relative, utc = _a.utc;
            callIfFunction_1.callIfFunction(_this.props.onChangeTime, { start: start, end: end, period: period, utc: utc });
        };
        _this.handleUpdateTime = function (_a) {
            var _b = _a === void 0 ? {} : _a, period = _b.relative, start = _b.start, end = _b.end, utc = _b.utc;
            var newValueObj = {
                period: period,
                start: start,
                end: end,
                utc: utc,
            };
            globalSelection_1.updateDateTime(newValueObj, _this.props.router, _this.getUpdateOptions());
            callIfFunction_1.callIfFunction(_this.props.onUpdateTime, newValueObj);
        };
        _this.handleUpdateEnvironmments = function () {
            var environments = _this.state.environments;
            globalSelection_1.updateEnvironments(environments, _this.props.router, _this.getUpdateOptions());
            _this.setState({ environments: null });
            callIfFunction_1.callIfFunction(_this.props.onUpdateEnvironments, environments);
        };
        _this.handleUpdateProjects = function () {
            var projects = _this.state.projects;
            // Clear environments when switching projects
            globalSelection_1.updateProjects(projects || [], _this.props.router, tslib_1.__assign(tslib_1.__assign({}, _this.getUpdateOptions()), { environments: [] }));
            _this.setState({ projects: null, environments: null });
            callIfFunction_1.callIfFunction(_this.props.onUpdateProjects, projects);
        };
        _this.getBackButton = function () {
            var _a = _this.props, organization = _a.organization, location = _a.location;
            return (<BackButtonWrapper>
        <tooltip_1.default title={locale_1.t('Back to Issues Stream')} position="bottom">
          <backToIssues_1.default data-test-id="back-to-issues" to={"/organizations/" + organization.slug + "/issues/" + location.search}>
            <icons_1.IconArrow direction="left" size="sm"/>
          </backToIssues_1.default>
        </tooltip_1.default>
      </BackButtonWrapper>);
        };
        _this.scrollFetchDispatcher = debounce_1.default(function (onSearch, options) {
            onSearch(_this.state.searchQuery, options);
        }, 200, { leading: true, trailing: false });
        _this.searchDispatcher = debounce_1.default(function (onSearch, searchQuery, options) {
            // in the case that a user repeats a search query (because search is
            // debounced this is possible if the user types and then deletes what they
            // typed) we should switch to an append strategy to not override all results
            // with a new page.
            if (_this.state.searchQuery === searchQuery) {
                options.append = true;
            }
            onSearch(searchQuery, options);
            _this.setState({
                searchQuery: searchQuery,
            });
        }, 200);
        return _this;
    }
    GlobalSelectionHeader.prototype.render = function () {
        var _this = this;
        var _a;
        var _b = this.props, className = _b.className, children = _b.children, shouldForceProject = _b.shouldForceProject, forceProject = _b.forceProject, isGlobalSelectionReady = _b.isGlobalSelectionReady, loadingProjects = _b.loadingProjects, organization = _b.organization, showAbsolute = _b.showAbsolute, showRelative = _b.showRelative, showDateSelector = _b.showDateSelector, showEnvironmentSelector = _b.showEnvironmentSelector, memberProjects = _b.memberProjects, nonMemberProjects = _b.nonMemberProjects, showIssueStreamLink = _b.showIssueStreamLink, showProjectSettingsLink = _b.showProjectSettingsLink, lockedMessageSubject = _b.lockedMessageSubject, timeRangeHint = _b.timeRangeHint, specificProjectSlugs = _b.specificProjectSlugs, disableMultipleProjectSelection = _b.disableMultipleProjectSelection, projectsFooterMessage = _b.projectsFooterMessage, defaultSelection = _b.defaultSelection;
        var _c = this.props.selection.datetime || {}, period = _c.period, start = _c.start, end = _c.end, utc = _c.utc;
        var defaultPeriod = ((_a = defaultSelection === null || defaultSelection === void 0 ? void 0 : defaultSelection.datetime) === null || _a === void 0 ? void 0 : _a.period) || constants_1.DEFAULT_STATS_PERIOD;
        var selectedProjects = forceProject
            ? [parseInt(forceProject.id, 10)]
            : this.props.selection.projects;
        return (<React.Fragment>
        <header_1.default className={className}>
          <headerItemPosition_1.default>
            {showIssueStreamLink && this.getBackButton()}
            <projects_1.default orgId={organization.slug} limit={PROJECTS_PER_PAGE} slugs={specificProjectSlugs}>
              {function (_a) {
                var projects = _a.projects, hasMore = _a.hasMore, onSearch = _a.onSearch, fetching = _a.fetching;
                var paginatedProjectSelectorCallbacks = {
                    onScroll: function (_a) {
                        var clientHeight = _a.clientHeight, scrollHeight = _a.scrollHeight, scrollTop = _a.scrollTop;
                        // check if no new projects are being fetched and the user has
                        // scrolled far enough to fetch a new page of projects
                        if (!fetching &&
                            scrollTop + clientHeight >= scrollHeight - clientHeight &&
                            hasMore) {
                            _this.scrollFetchDispatcher(onSearch, { append: true });
                        }
                    },
                    onFilterChange: function (event) {
                        _this.searchDispatcher(onSearch, event.target.value, {
                            append: false,
                        });
                    },
                    searching: fetching,
                    paginated: true,
                };
                return (<multipleProjectSelector_1.default organization={organization} shouldForceProject={shouldForceProject} forceProject={forceProject} projects={loadingProjects ? projects : memberProjects} isGlobalSelectionReady={isGlobalSelectionReady} nonMemberProjects={nonMemberProjects} value={_this.state.projects || _this.props.selection.projects} onChange={_this.handleChangeProjects} onUpdate={_this.handleUpdateProjects} multi={!disableMultipleProjectSelection &&
                        _this.hasMultipleProjectSelection()} {...(loadingProjects ? paginatedProjectSelectorCallbacks : {})} showIssueStreamLink={showIssueStreamLink} showProjectSettingsLink={showProjectSettingsLink} lockedMessageSubject={lockedMessageSubject} footerMessage={projectsFooterMessage}/>);
            }}
            </projects_1.default>
          </headerItemPosition_1.default>

          {showEnvironmentSelector && (<React.Fragment>
              <headerSeparator_1.default />
              <headerItemPosition_1.default>
                <multipleEnvironmentSelector_1.default organization={organization} projects={this.props.projects} loadingProjects={loadingProjects} selectedProjects={selectedProjects} value={this.props.selection.environments} onChange={this.handleChangeEnvironments} onUpdate={this.handleUpdateEnvironmments}/>
              </headerItemPosition_1.default>
            </React.Fragment>)}

          {showDateSelector && (<React.Fragment>
              <headerSeparator_1.default />
              <headerItemPosition_1.default>
                <timeRangeSelector_1.default key={"period:" + period + "-start:" + start + "-end:" + end + "-utc:" + utc + "-defaultPeriod:" + defaultPeriod} showAbsolute={showAbsolute} showRelative={showRelative} relative={period} start={start} end={end} utc={utc} onChange={this.handleChangeTime} onUpdate={this.handleUpdateTime} organization={organization} defaultPeriod={defaultPeriod} hint={timeRangeHint}/>
              </headerItemPosition_1.default>
            </React.Fragment>)}

          {!showEnvironmentSelector && <headerItemPosition_1.default isSpacer/>}
          {!showDateSelector && <headerItemPosition_1.default isSpacer/>}
        </header_1.default>

        {isGlobalSelectionReady ? children : <organization_1.PageContent />}
      </React.Fragment>);
    };
    GlobalSelectionHeader.defaultProps = defaultProps;
    return GlobalSelectionHeader;
}(React.Component));
exports.default = withGlobalSelection_1.default(GlobalSelectionHeader);
var BackButtonWrapper = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: relative;\n  left: ", ";\n"], ["\n  display: flex;\n  align-items: center;\n  height: 100%;\n  position: relative;\n  left: ", ";\n"])), space_1.default(2));
var templateObject_1;
//# sourceMappingURL=globalSelectionHeader.jsx.map
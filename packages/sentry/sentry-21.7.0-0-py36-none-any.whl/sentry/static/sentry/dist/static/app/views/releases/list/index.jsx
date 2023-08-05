Object.defineProperty(exports, "__esModule", { value: true });
exports.ReleasesList = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_lazyload_1 = require("react-lazyload");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var tags_1 = require("app/actionCreators/tags");
var feature_1 = tslib_1.__importDefault(require("app/components/acl/feature"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var utils_1 = require("app/components/organizations/timeRangeSelector/utils");
var pageHeading_1 = tslib_1.__importDefault(require("app/components/pageHeading"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var smartSearchBar_1 = tslib_1.__importDefault(require("app/components/smartSearchBar"));
var constants_1 = require("app/constants");
var globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
var platformCategories_1 = require("app/data/platformCategories");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var types_1 = require("app/types");
var analytics_1 = require("app/utils/analytics");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var releaseArchivedNotice_1 = tslib_1.__importDefault(require("../detail/overview/releaseArchivedNotice"));
var releaseHealthRequest_1 = tslib_1.__importDefault(require("../utils/releaseHealthRequest"));
var releaseAdoptionChart_1 = tslib_1.__importDefault(require("./releaseAdoptionChart"));
var releaseCard_1 = tslib_1.__importDefault(require("./releaseCard"));
var releaseDisplayOptions_1 = tslib_1.__importDefault(require("./releaseDisplayOptions"));
var releaseListSortOptions_1 = tslib_1.__importDefault(require("./releaseListSortOptions"));
var releaseListStatusOptions_1 = tslib_1.__importDefault(require("./releaseListStatusOptions"));
var releasePromo_1 = tslib_1.__importDefault(require("./releasePromo"));
var utils_2 = require("./utils");
var supportedTags = {
    'release.version': {
        key: 'release.version',
        name: 'release.version',
    },
    'release.build': {
        key: 'release.build',
        name: 'release.build',
    },
    'release.package': {
        key: 'release.package',
        name: 'release.package',
    },
    release: {
        key: 'release',
        name: 'release',
    },
};
var ReleasesList = /** @class */ (function (_super) {
    tslib_1.__extends(ReleasesList, _super);
    function ReleasesList() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        _this.shouldRenderBadRequests = true;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleSortBy = function (sort) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, sort: sort }) }));
        };
        _this.handleDisplay = function (display) {
            var _a = _this.props, location = _a.location, router = _a.router;
            var sort = location.query.sort;
            if (sort === utils_2.SortOption.USERS_24_HOURS && display === utils_2.DisplayOption.SESSIONS)
                sort = utils_2.SortOption.SESSIONS_24_HOURS;
            else if (sort === utils_2.SortOption.SESSIONS_24_HOURS && display === utils_2.DisplayOption.USERS)
                sort = utils_2.SortOption.USERS_24_HOURS;
            else if (sort === utils_2.SortOption.CRASH_FREE_USERS && display === utils_2.DisplayOption.SESSIONS)
                sort = utils_2.SortOption.CRASH_FREE_SESSIONS;
            else if (sort === utils_2.SortOption.CRASH_FREE_SESSIONS && display === utils_2.DisplayOption.USERS)
                sort = utils_2.SortOption.CRASH_FREE_USERS;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, display: display, sort: sort }) }));
        };
        _this.handleStatus = function (status) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, status: status }) }));
        };
        _this.trackAddReleaseHealth = function () {
            var _a = _this.props, organization = _a.organization, selection = _a.selection;
            if (organization.id && selection.projects[0]) {
                analytics_1.trackAnalyticsEvent({
                    eventKey: "releases_list.click_add_release_health",
                    eventName: "Releases List: Click Add Release Health",
                    organization_id: parseInt(organization.id, 10),
                    project_id: selection.projects[0],
                });
            }
        };
        _this.tagValueLoader = function (key, search) {
            var _a = _this.props, location = _a.location, organization = _a.organization;
            var projectId = location.query.project;
            return tags_1.fetchTagValues(_this.api, organization.slug, key, search, projectId ? [projectId] : null, location.query);
        };
        _this.getTagValues = function (tag, currentQuery) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var values;
            return tslib_1.__generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, this.tagValueLoader(tag.key, currentQuery)];
                    case 1:
                        values = _a.sent();
                        return [2 /*return*/, values.map(function (_a) {
                                var value = _a.value;
                                return value;
                            })];
                }
            });
        }); };
        return _this;
    }
    ReleasesList.prototype.getTitle = function () {
        return routeTitle_1.default(locale_1.t('Releases'), this.props.organization.slug, false);
    };
    ReleasesList.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, location = _a.location;
        var statsPeriod = location.query.statsPeriod;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var query = tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, ['project', 'environment', 'cursor', 'query', 'sort'])), { summaryStatsPeriod: statsPeriod, per_page: 20, flatten: activeSort === utils_2.SortOption.DATE ? 0 : 1, adoptionStages: 1, status: activeStatus === utils_2.StatusOption.ARCHIVED
                ? types_1.ReleaseStatus.Archived
                : types_1.ReleaseStatus.Active });
        var endpoints = [
            [
                'releases',
                "/organizations/" + organization.slug + "/releases/",
                { query: query },
                { disableEntireQuery: true },
            ],
        ];
        return endpoints;
    };
    ReleasesList.prototype.componentDidMount = function () {
        if (this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
    };
    ReleasesList.prototype.componentDidUpdate = function (prevProps, prevState) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
        if (prevProps.location.query.project !== this.props.location.query.project) {
            this.fetchSessionsExistence();
        }
        if (prevState.releases !== this.state.releases) {
            /**
             * Manually trigger checking for elements in viewport.
             * Helpful when LazyLoad components enter the viewport without resize or scroll events,
             * https://github.com/twobin/react-lazyload#forcecheck
             *
             * HealthStatsCharts are being rendered only when they are scrolled into viewport.
             * This is how we re-check them without scrolling once releases change as this view
             * uses shouldReload=true and there is no reloading happening.
             */
            react_lazyload_1.forceCheck();
        }
    };
    ReleasesList.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ReleasesList.prototype.getSort = function () {
        var sort = this.props.location.query.sort;
        switch (sort) {
            case utils_2.SortOption.CRASH_FREE_USERS:
                return utils_2.SortOption.CRASH_FREE_USERS;
            case utils_2.SortOption.CRASH_FREE_SESSIONS:
                return utils_2.SortOption.CRASH_FREE_SESSIONS;
            case utils_2.SortOption.SESSIONS:
                return utils_2.SortOption.SESSIONS;
            case utils_2.SortOption.USERS_24_HOURS:
                return utils_2.SortOption.USERS_24_HOURS;
            case utils_2.SortOption.SESSIONS_24_HOURS:
                return utils_2.SortOption.SESSIONS_24_HOURS;
            case utils_2.SortOption.BUILD:
                return utils_2.SortOption.BUILD;
            case utils_2.SortOption.SEMVER:
                return utils_2.SortOption.SEMVER;
            case utils_2.SortOption.ADOPTION:
                return utils_2.SortOption.ADOPTION;
            default:
                return utils_2.SortOption.DATE;
        }
    };
    ReleasesList.prototype.getDisplay = function () {
        var display = this.props.location.query.display;
        switch (display) {
            case utils_2.DisplayOption.USERS:
                return utils_2.DisplayOption.USERS;
            default:
                return utils_2.DisplayOption.SESSIONS;
        }
    };
    ReleasesList.prototype.getStatus = function () {
        var status = this.props.location.query.status;
        switch (status) {
            case utils_2.StatusOption.ARCHIVED:
                return utils_2.StatusOption.ARCHIVED;
            default:
                return utils_2.StatusOption.ACTIVE;
        }
    };
    ReleasesList.prototype.getSelectedProject = function () {
        var _a;
        var _b = this.props, selection = _b.selection, organization = _b.organization;
        var selectedProjectId = selection.projects && selection.projects.length === 1 && selection.projects[0];
        return (_a = organization.projects) === null || _a === void 0 ? void 0 : _a.find(function (p) { return p.id === "" + selectedProjectId; });
    };
    ReleasesList.prototype.fetchSessionsExistence = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _a, organization, location, projectId, response, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, organization = _a.organization, location = _a.location;
                        projectId = location.query.project;
                        if (!projectId) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            hasSessions: null,
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/organizations/" + organization.slug + "/sessions/", {
                                query: {
                                    project: projectId,
                                    field: 'sum(session)',
                                    statsPeriod: '90d',
                                    interval: '1d',
                                },
                            })];
                    case 2:
                        response = _c.sent();
                        this.setState({
                            hasSessions: response.groups[0].totals['sum(session)'] > 0,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ReleasesList.prototype.shouldShowLoadingIndicator = function () {
        var _a = this.state, loading = _a.loading, releases = _a.releases, reloading = _a.reloading;
        return (loading && !reloading) || (loading && !(releases === null || releases === void 0 ? void 0 : releases.length));
    };
    ReleasesList.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderError = function () {
        return this.renderBody();
    };
    ReleasesList.prototype.renderEmptyMessage = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, selection = _a.selection;
        var statsPeriod = location.query.statsPeriod;
        var searchQuery = this.getQuery();
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        if (searchQuery && searchQuery.length) {
            return (<emptyStateWarning_1.default small>{locale_1.t('There are no releases that match') + ": '" + searchQuery + "'."}</emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.USERS_24_HOURS) {
            return (<emptyStateWarning_1.default small>
          {locale_1.t('There are no releases with active user data (users in the last 24 hours).')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.SESSIONS_24_HOURS) {
            return (<emptyStateWarning_1.default small>
          {locale_1.t('There are no releases with active session data (sessions in the last 24 hours).')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort === utils_2.SortOption.BUILD || activeSort === utils_2.SortOption.SEMVER) {
            return (<emptyStateWarning_1.default small>
          {locale_1.t('There are no releases with semantic versioning.')}
        </emptyStateWarning_1.default>);
        }
        if (activeSort !== utils_2.SortOption.DATE) {
            var relativePeriod = utils_1.getRelativeSummary(statsPeriod || constants_1.DEFAULT_STATS_PERIOD).toLowerCase();
            return (<emptyStateWarning_1.default small>
          {locale_1.t('There are no releases with data in the') + " " + relativePeriod + "."}
        </emptyStateWarning_1.default>);
        }
        if (activeStatus === utils_2.StatusOption.ARCHIVED) {
            return (<emptyStateWarning_1.default small>
          {locale_1.t('There are no archived releases.')}
        </emptyStateWarning_1.default>);
        }
        return (<releasePromo_1.default organization={organization} projectId={selection.projects.filter(function (p) { return p !== globalSelectionHeader_2.ALL_ACCESS_PROJECTS; })[0]}/>);
    };
    ReleasesList.prototype.renderHealthCta = function () {
        var _this = this;
        var organization = this.props.organization;
        var _a = this.state, hasSessions = _a.hasSessions, releases = _a.releases;
        var selectedProject = this.getSelectedProject();
        if (!selectedProject || hasSessions !== false || !(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return null;
        }
        return (<projects_1.default orgId={organization.slug} slugs={[selectedProject.slug]}>
        {function (_a) {
                var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, fetchError = _a.fetchError;
                var project = projects && projects.length === 1 && projects[0];
                var projectCanHaveReleases = project && project.platform && platformCategories_1.releaseHealth.includes(project.platform);
                if (!initiallyLoaded || fetchError || !projectCanHaveReleases) {
                    return null;
                }
                return (<alert_1.default type="info" icon={<icons_1.IconInfo size="md"/>}>
              <AlertText>
                <div>
                  {locale_1.t('To track user adoption, crash rates, session data and more, add Release Health to your current setup.')}
                </div>
                <externalLink_1.default href="https://docs.sentry.io/product/releases/health/setup/" onClick={_this.trackAddReleaseHealth}>
                  {locale_1.t('Add Release Health')}
                </externalLink_1.default>
              </AlertText>
            </alert_1.default>);
            }}
      </projects_1.default>);
    };
    ReleasesList.prototype.renderInnerBody = function (activeDisplay) {
        var _this = this;
        var _a = this.props, location = _a.location, selection = _a.selection, organization = _a.organization, router = _a.router;
        var _b = this.state, hasSessions = _b.hasSessions, releases = _b.releases, reloading = _b.reloading, releasesPageLinks = _b.releasesPageLinks;
        if (this.shouldShowLoadingIndicator()) {
            return <loadingIndicator_1.default />;
        }
        if (!(releases === null || releases === void 0 ? void 0 : releases.length)) {
            return this.renderEmptyMessage();
        }
        return (<releaseHealthRequest_1.default releases={releases.map(function (_a) {
            var version = _a.version;
            return version;
        })} organization={organization} selection={selection} location={location} display={[this.getDisplay()]} releasesReloading={reloading} healthStatsPeriod={location.query.healthStatsPeriod}>
        {function (_a) {
                var _b;
                var isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData;
                var singleProjectSelected = ((_b = selection.projects) === null || _b === void 0 ? void 0 : _b.length) === 1 &&
                    selection.projects[0] !== globalSelectionHeader_2.ALL_ACCESS_PROJECTS;
                var selectedProject = _this.getSelectedProject();
                var isMobileProject = selectedProject &&
                    selectedProject.platform &&
                    tslib_1.__spreadArray(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(platformCategories_1.mobile)), tslib_1.__read(platformCategories_1.desktop)), [
                        'java-android',
                        'cocoa-objc',
                        'cocoa-swift',
                    ]).includes(selectedProject.platform);
                return (<react_1.Fragment>
              {singleProjectSelected && hasSessions && isMobileProject && (<feature_1.default features={['organizations:release-adoption-chart']}>
                  <releaseAdoptionChart_1.default organization={organization} selection={selection} location={location} router={router} activeDisplay={activeDisplay}/>
                </feature_1.default>)}

              {releases.map(function (release, index) { return (<releaseCard_1.default key={release.version + "-" + release.projects[0].slug} activeDisplay={activeDisplay} release={release} organization={organization} location={location} selection={selection} reloading={reloading} showHealthPlaceholders={isHealthLoading} isTopRelease={index === 0} getHealthData={getHealthData}/>); })}
              <pagination_1.default pageLinks={releasesPageLinks}/>
            </react_1.Fragment>);
            }}
      </releaseHealthRequest_1.default>);
    };
    ReleasesList.prototype.renderBody = function () {
        var organization = this.props.organization;
        var _a = this.state, releases = _a.releases, reloading = _a.reloading, error = _a.error;
        var activeSort = this.getSort();
        var activeStatus = this.getStatus();
        var activeDisplay = this.getDisplay();
        var hasSemver = organization.features.includes('semver');
        return (<globalSelectionHeader_1.default showAbsolute={false} timeRangeHint={locale_1.t('Changing this date range will recalculate the release metrics.')}>
        <organization_1.PageContent>
          <lightWeightNoProjectMessage_1.default organization={organization}>
            <organization_1.PageHeader>
              <pageHeading_1.default>{locale_1.t('Releases')}</pageHeading_1.default>
            </organization_1.PageHeader>

            {this.renderHealthCta()}

            <SortAndFilterWrapper>
              {hasSemver ? (<smartSearchBar_1.default searchSource="releases" query={this.getQuery()} placeholder={locale_1.t('Search by release version')} maxSearchItems={5} hasRecentSearches={false} supportedTags={supportedTags} onSearch={this.handleSearch} onGetTagValues={this.getTagValues}/>) : (<searchBar_1.default placeholder={locale_1.t('Search')} onSearch={this.handleSearch} query={this.getQuery()}/>)}
              <releaseListStatusOptions_1.default selected={activeStatus} onSelect={this.handleStatus}/>
              <releaseListSortOptions_1.default selected={activeSort} selectedDisplay={activeDisplay} onSelect={this.handleSortBy} organization={organization}/>
              <releaseDisplayOptions_1.default selected={activeDisplay} onSelect={this.handleDisplay}/>
            </SortAndFilterWrapper>

            {!reloading &&
                activeStatus === utils_2.StatusOption.ARCHIVED &&
                !!(releases === null || releases === void 0 ? void 0 : releases.length) && <releaseArchivedNotice_1.default multi/>}

            {error
                ? _super.prototype.renderError.call(this, new Error('Unable to load all required endpoints'))
                : this.renderInnerBody(activeDisplay)}
          </lightWeightNoProjectMessage_1.default>
        </organization_1.PageContent>
      </globalSelectionHeader_1.default>);
    };
    return ReleasesList;
}(asyncView_1.default));
exports.ReleasesList = ReleasesList;
var AlertText = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: flex-start;\n  justify-content: flex-start;\n  gap: ", ";\n\n  > *:nth-child(1) {\n    flex: 1;\n  }\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-direction: row;\n  }\n"], ["\n  display: flex;\n  align-items: flex-start;\n  justify-content: flex-start;\n  gap: ", ";\n\n  > *:nth-child(1) {\n    flex: 1;\n  }\n  flex-direction: column;\n  @media (min-width: ", ") {\n    flex-direction: row;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[1]; });
var SortAndFilterWrapper = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"], ["\n  display: inline-grid;\n  grid-gap: ", ";\n  margin-bottom: ", ";\n\n  @media (min-width: ", ") {\n    grid-template-columns: 1fr repeat(3, auto);\n  }\n"])), space_1.default(2), space_1.default(2), function (p) { return p.theme.breakpoints[1]; });
exports.default = withOrganization_1.default(withGlobalSelection_1.default(ReleasesList));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
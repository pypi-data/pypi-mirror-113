Object.defineProperty(exports, "__esModule", { value: true });
exports.ReleasesDetailContainer = exports.ReleaseContext = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var moment_1 = tslib_1.__importDefault(require("moment"));
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var lightWeightNoProjectMessage_1 = tslib_1.__importDefault(require("app/components/lightWeightNoProjectMessage"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var globalSelectionHeader_1 = tslib_1.__importDefault(require("app/components/organizations/globalSelectionHeader"));
var getParams_1 = require("app/components/organizations/globalSelectionHeader/getParams");
var pickProjectToContinue_1 = tslib_1.__importDefault(require("app/components/pickProjectToContinue"));
var constants_1 = require("app/constants");
var globalSelectionHeader_2 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var utils_1 = require("../list/utils");
var utils_2 = require("../utils");
var releaseHealthRequest_1 = tslib_1.__importDefault(require("../utils/releaseHealthRequest"));
var releaseHeader_1 = tslib_1.__importDefault(require("./releaseHeader"));
var DEFAULT_FRESH_RELEASE_STATS_PERIOD = '24h';
var ReleaseContext = react_1.createContext({});
exports.ReleaseContext = ReleaseContext;
var ReleasesDetail = /** @class */ (function (_super) {
    tslib_1.__extends(ReleasesDetail, _super);
    function ReleasesDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetail.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, organization = _a.organization, selection = _a.selection;
        var release = this.state.release;
        // The release details page will always have only one project selected
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        return routeTitle_1.default(locale_1.t('Release %s', formatters_1.formatVersion(params.release)), organization.slug, false, project === null || project === void 0 ? void 0 : project.slug);
    };
    ReleasesDetail.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { deploys: [], sessions: null });
    };
    ReleasesDetail.prototype.getEndpoints = function () {
        var _a;
        var _b = this.props, organization = _b.organization, location = _b.location, params = _b.params, releaseMeta = _b.releaseMeta, defaultStatsPeriod = _b.defaultStatsPeriod;
        var basePath = "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/";
        var endpoints = [
            [
                'release',
                basePath,
                {
                    query: tslib_1.__assign({ adoptionStages: 1 }, getParams_1.getParams(pick_1.default(location.query, tslib_1.__spreadArray([], tslib_1.__read(Object.values(globalSelectionHeader_2.URL_PARAM)))), {
                        defaultStatsPeriod: defaultStatsPeriod,
                    })),
                },
            ],
        ];
        if (releaseMeta.deployCount > 0) {
            endpoints.push(['deploys', basePath + "deploys/"]);
        }
        // Used to figure out if the release has any health data
        endpoints.push([
            'sessions',
            "/organizations/" + organization.slug + "/sessions/",
            {
                query: {
                    project: location.query.project,
                    environment: (_a = location.query.environment) !== null && _a !== void 0 ? _a : [],
                    query: "release:\"" + params.release + "\"",
                    field: 'sum(session)',
                    statsPeriod: '90d',
                    interval: '1d',
                },
            },
        ]);
        return endpoints;
    };
    ReleasesDetail.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var possiblyWrongProject = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404 || (e === null || e === void 0 ? void 0 : e.status) === 403; });
        if (possiblyWrongProject) {
            return (<organization_1.PageContent>
          <alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {locale_1.t('This release may not be in your selected project.')}
          </alert_1.default>
        </organization_1.PageContent>);
        }
        return _super.prototype.renderError.apply(this, tslib_1.__spreadArray([], tslib_1.__read(args)));
    };
    ReleasesDetail.prototype.renderLoading = function () {
        return (<organization_1.PageContent>
        <loadingIndicator_1.default />
      </organization_1.PageContent>);
    };
    ReleasesDetail.prototype.renderBody = function () {
        var _a = this.props, organization = _a.organization, location = _a.location, selection = _a.selection, releaseMeta = _a.releaseMeta, defaultStatsPeriod = _a.defaultStatsPeriod, getHealthData = _a.getHealthData, isHealthLoading = _a.isHealthLoading;
        var _b = this.state, release = _b.release, deploys = _b.deploys, sessions = _b.sessions, reloading = _b.reloading;
        var project = release === null || release === void 0 ? void 0 : release.projects.find(function (p) { return p.id === selection.projects[0]; });
        var releaseBounds = utils_2.getReleaseBounds(release);
        if (!project || !release) {
            if (reloading) {
                return <loadingIndicator_1.default />;
            }
            return null;
        }
        return (<lightWeightNoProjectMessage_1.default organization={organization}>
        <StyledPageContent>
          <releaseHeader_1.default location={location} organization={organization} release={release} project={project} releaseMeta={releaseMeta} refetchData={this.fetchData}/>
          <ReleaseContext.Provider value={{
                release: release,
                project: project,
                deploys: deploys,
                releaseMeta: releaseMeta,
                refetchData: this.fetchData,
                defaultStatsPeriod: defaultStatsPeriod,
                getHealthData: getHealthData,
                isHealthLoading: isHealthLoading,
                hasHealthData: !!(sessions === null || sessions === void 0 ? void 0 : sessions.groups[0].totals['sum(session)']),
                releaseBounds: releaseBounds,
            }}>
            {this.props.children}
          </ReleaseContext.Provider>
        </StyledPageContent>
      </lightWeightNoProjectMessage_1.default>);
    };
    return ReleasesDetail;
}(asyncView_1.default));
var ReleasesDetailContainer = /** @class */ (function (_super) {
    tslib_1.__extends(ReleasesDetailContainer, _super);
    function ReleasesDetailContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.shouldReload = true;
        return _this;
    }
    ReleasesDetailContainer.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params;
        // fetch projects this release belongs to
        return [
            [
                'releaseMeta',
                "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/meta/",
            ],
        ];
    };
    Object.defineProperty(ReleasesDetailContainer.prototype, "hasReleaseComparison", {
        get: function () {
            return this.props.organization.features.includes('release-comparison');
        },
        enumerable: false,
        configurable: true
    });
    ReleasesDetailContainer.prototype.componentDidMount = function () {
        this.removeGlobalDateTimeFromUrl();
    };
    ReleasesDetailContainer.prototype.componentDidUpdate = function (prevProps, prevContext) {
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
        this.removeGlobalDateTimeFromUrl();
    };
    ReleasesDetailContainer.prototype.removeGlobalDateTimeFromUrl = function () {
        var _a = this.props, router = _a.router, location = _a.location;
        var _b = location.query, start = _b.start, end = _b.end, statsPeriod = _b.statsPeriod, utc = _b.utc, restQuery = tslib_1.__rest(_b, ["start", "end", "statsPeriod", "utc"]);
        if (!this.hasReleaseComparison) {
            return;
        }
        if (start || end || statsPeriod || utc) {
            router.replace(tslib_1.__assign(tslib_1.__assign({}, location), { query: restQuery }));
        }
    };
    ReleasesDetailContainer.prototype.renderError = function () {
        var args = [];
        for (var _i = 0; _i < arguments.length; _i++) {
            args[_i] = arguments[_i];
        }
        var has404Errors = Object.values(this.state.errors).find(function (e) { return (e === null || e === void 0 ? void 0 : e.status) === 404; });
        if (has404Errors) {
            // This catches a 404 coming from the release endpoint and displays a custom error message.
            return (<organization_1.PageContent>
          <alert_1.default type="error" icon={<icons_1.IconWarning />}>
            {locale_1.t('This release could not be found.')}
          </alert_1.default>
        </organization_1.PageContent>);
        }
        return _super.prototype.renderError.apply(this, tslib_1.__spreadArray([], tslib_1.__read(args)));
    };
    ReleasesDetailContainer.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    ReleasesDetailContainer.prototype.renderLoading = function () {
        return (<organization_1.PageContent>
        <loadingIndicator_1.default />
      </organization_1.PageContent>);
    };
    ReleasesDetailContainer.prototype.renderProjectsFooterMessage = function () {
        return (<ProjectsFooterMessage>
        <icons_1.IconInfo size="xs"/> {locale_1.t('Only projects with this release are visible.')}
      </ProjectsFooterMessage>);
    };
    ReleasesDetailContainer.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, params = _a.params, router = _a.router, location = _a.location, selection = _a.selection;
        var releaseMeta = this.state.releaseMeta;
        if (!releaseMeta) {
            return null;
        }
        var projects = releaseMeta.projects;
        var isFreshRelease = moment_1.default(releaseMeta.released).isAfter(moment_1.default().subtract(24, 'hours'));
        var defaultStatsPeriod = isFreshRelease
            ? DEFAULT_FRESH_RELEASE_STATS_PERIOD
            : constants_1.DEFAULT_STATS_PERIOD;
        if (this.isProjectMissingInUrl()) {
            return (<pickProjectToContinue_1.default projects={projects.map(function (_a) {
                    var id = _a.id, slug = _a.slug;
                    return ({
                        id: String(id),
                        slug: slug,
                    });
                })} router={router} nextPath={{
                    pathname: "/organizations/" + organization.slug + "/releases/" + encodeURIComponent(params.release) + "/",
                }} noProjectRedirectPath={"/organizations/" + organization.slug + "/releases/"}/>);
        }
        return (<globalSelectionHeader_1.default lockedMessageSubject={locale_1.t('release')} shouldForceProject={projects.length === 1} forceProject={projects.length === 1 ? tslib_1.__assign(tslib_1.__assign({}, projects[0]), { id: String(projects[0].id) }) : undefined} specificProjectSlugs={projects.map(function (p) { return p.slug; })} disableMultipleProjectSelection showProjectSettingsLink projectsFooterMessage={this.renderProjectsFooterMessage()} defaultSelection={{
                datetime: {
                    start: null,
                    end: null,
                    utc: false,
                    period: defaultStatsPeriod,
                },
            }} showDateSelector={!this.hasReleaseComparison}>
        <releaseHealthRequest_1.default releases={[params.release]} organization={organization} selection={selection} location={location} display={[utils_1.DisplayOption.SESSIONS, utils_1.DisplayOption.USERS]} defaultStatsPeriod={defaultStatsPeriod} disable={this.hasReleaseComparison}>
          {function (_a) {
                var isHealthLoading = _a.isHealthLoading, getHealthData = _a.getHealthData;
                return (<ReleasesDetail {..._this.props} releaseMeta={releaseMeta} defaultStatsPeriod={defaultStatsPeriod} getHealthData={getHealthData} isHealthLoading={isHealthLoading}/>);
            }}
        </releaseHealthRequest_1.default>
      </globalSelectionHeader_1.default>);
    };
    return ReleasesDetailContainer;
}(asyncComponent_1.default));
exports.ReleasesDetailContainer = ReleasesDetailContainer;
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var ProjectsFooterMessage = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  align-items: center;\n  grid-template-columns: min-content 1fr;\n  grid-gap: ", ";\n"])), space_1.default(1));
exports.default = withGlobalSelection_1.default(withOrganization_1.default(ReleasesDetailContainer));
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
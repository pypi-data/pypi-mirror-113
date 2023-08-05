Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var projects_1 = require("app/actionCreators/projects");
var asyncComponent_1 = tslib_1.__importDefault(require("app/components/asyncComponent"));
var styles_1 = require("app/components/charts/styles");
var dateTime_1 = tslib_1.__importDefault(require("app/components/dateTime"));
var emptyStateWarning_1 = tslib_1.__importDefault(require("app/components/emptyStateWarning"));
var placeholder_1 = tslib_1.__importDefault(require("app/components/placeholder"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var overflowEllipsis_1 = tslib_1.__importDefault(require("app/styles/overflowEllipsis"));
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var analytics_1 = require("app/utils/analytics");
var releasePromo_1 = require("app/views/releases/list/releasePromo");
var missingReleasesButtons_1 = tslib_1.__importDefault(require("./missingFeatureButtons/missingReleasesButtons"));
var styles_2 = require("./styles");
var utils_1 = require("./utils");
var PLACEHOLDER_AND_EMPTY_HEIGHT = '160px';
var ProjectLatestReleases = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectLatestReleases, _super);
    function ProjectLatestReleases() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleTourAdvance = function (index) {
            var _a = _this.props, organization = _a.organization, projectId = _a.projectId;
            analytics_1.analytics('releases.landing_card_clicked', {
                org_id: parseInt(organization.id, 10),
                project_id: projectId && parseInt(projectId, 10),
                step_id: index,
                step_title: releasePromo_1.RELEASES_TOUR_STEPS[index].title,
            });
        };
        _this.renderReleaseRow = function (release) {
            var projectId = _this.props.projectId;
            var lastDeploy = release.lastDeploy, dateCreated = release.dateCreated;
            return (<react_1.Fragment key={release.version}>
        <dateTime_1.default date={(lastDeploy === null || lastDeploy === void 0 ? void 0 : lastDeploy.dateFinished) || dateCreated} seconds={false}/>
        <textOverflow_1.default>
          <StyledVersion version={release.version} tooltipRawVersion projectId={projectId}/>
        </textOverflow_1.default>
      </react_1.Fragment>);
        };
        return _this;
    }
    ProjectLatestReleases.prototype.shouldComponentUpdate = function (nextProps, nextState) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        // TODO(project-detail): we temporarily removed refetching based on timeselector
        if (this.state !== nextState ||
            utils_1.didProjectOrEnvironmentChange(location, nextProps.location) ||
            isProjectStabilized !== nextProps.isProjectStabilized) {
            return true;
        }
        return false;
    };
    ProjectLatestReleases.prototype.componentDidUpdate = function (prevProps) {
        var _a = this.props, location = _a.location, isProjectStabilized = _a.isProjectStabilized;
        if (utils_1.didProjectOrEnvironmentChange(prevProps.location, location) ||
            prevProps.isProjectStabilized !== isProjectStabilized) {
            this.remountComponent();
        }
    };
    ProjectLatestReleases.prototype.getEndpoints = function () {
        var _a = this.props, location = _a.location, organization = _a.organization, projectSlug = _a.projectSlug, isProjectStabilized = _a.isProjectStabilized;
        if (!isProjectStabilized) {
            return [];
        }
        var query = tslib_1.__assign(tslib_1.__assign({}, pick_1.default(location.query, Object.values(globalSelectionHeader_1.URL_PARAM))), { per_page: 5 });
        // TODO(project-detail): this does not filter releases for the given time
        return [
            ['releases', "/projects/" + organization.slug + "/" + projectSlug + "/releases/", { query: query }],
        ];
    };
    /**
     * If our releases are empty, determine if we had a release in the last 90 days (empty message differs then)
     */
    ProjectLatestReleases.prototype.onLoadAllEndpointsSuccess = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var releases, _a, organization, projectId, isProjectStabilized, hasOlderReleases;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        releases = this.state.releases;
                        _a = this.props, organization = _a.organization, projectId = _a.projectId, isProjectStabilized = _a.isProjectStabilized;
                        if (!isProjectStabilized) {
                            return [2 /*return*/];
                        }
                        if ((releases !== null && releases !== void 0 ? releases : []).length !== 0 || !projectId) {
                            this.setState({ hasOlderReleases: true });
                            return [2 /*return*/];
                        }
                        this.setState({ loading: true });
                        return [4 /*yield*/, projects_1.fetchAnyReleaseExistence(this.api, organization.slug, projectId)];
                    case 1:
                        hasOlderReleases = _b.sent();
                        this.setState({ hasOlderReleases: hasOlderReleases, loading: false });
                        return [2 /*return*/];
                }
            });
        });
    };
    Object.defineProperty(ProjectLatestReleases.prototype, "releasesLink", {
        get: function () {
            var organization = this.props.organization;
            // as this is a link to latest releases, we want to only preserve project and environment
            return {
                pathname: "/organizations/" + organization.slug + "/releases/",
                query: {
                    statsPeriod: undefined,
                    start: undefined,
                    end: undefined,
                    utc: undefined,
                },
            };
        },
        enumerable: false,
        configurable: true
    });
    ProjectLatestReleases.prototype.renderInnerBody = function () {
        var _a = this.props, organization = _a.organization, projectId = _a.projectId, isProjectStabilized = _a.isProjectStabilized;
        var _b = this.state, loading = _b.loading, releases = _b.releases, hasOlderReleases = _b.hasOlderReleases;
        var checkingForOlderReleases = !(releases !== null && releases !== void 0 ? releases : []).length && hasOlderReleases === undefined;
        var showLoadingIndicator = loading || checkingForOlderReleases || !isProjectStabilized;
        if (showLoadingIndicator) {
            return <placeholder_1.default height={PLACEHOLDER_AND_EMPTY_HEIGHT}/>;
        }
        if (!hasOlderReleases) {
            return <missingReleasesButtons_1.default organization={organization} projectId={projectId}/>;
        }
        if (!releases || releases.length === 0) {
            return (<StyledEmptyStateWarning small>{locale_1.t('No releases found')}</StyledEmptyStateWarning>);
        }
        return <ReleasesTable>{releases.map(this.renderReleaseRow)}</ReleasesTable>;
    };
    ProjectLatestReleases.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectLatestReleases.prototype.renderBody = function () {
        return (<styles_2.SidebarSection>
        <styles_2.SectionHeadingWrapper>
          <styles_1.SectionHeading>{locale_1.t('Latest Releases')}</styles_1.SectionHeading>
          <styles_2.SectionHeadingLink to={this.releasesLink}>
            <icons_1.IconOpen />
          </styles_2.SectionHeadingLink>
        </styles_2.SectionHeadingWrapper>
        <div>{this.renderInnerBody()}</div>
      </styles_2.SidebarSection>);
    };
    return ProjectLatestReleases;
}(asyncComponent_1.default));
var ReleasesTable = styled_1.default('div')(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  font-size: ", ";\n  white-space: nowrap;\n  grid-template-columns: 1fr auto;\n  margin-bottom: ", ";\n\n  & > * {\n    padding: ", " ", ";\n    height: 32px;\n  }\n\n  & > *:nth-child(2n + 2) {\n    text-align: right;\n  }\n\n  & > *:nth-child(4n + 1),\n  & > *:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"], ["\n  display: grid;\n  font-size: ", ";\n  white-space: nowrap;\n  grid-template-columns: 1fr auto;\n  margin-bottom: ", ";\n\n  & > * {\n    padding: ", " ", ";\n    height: 32px;\n  }\n\n  & > *:nth-child(2n + 2) {\n    text-align: right;\n  }\n\n  & > *:nth-child(4n + 1),\n  & > *:nth-child(4n + 2) {\n    background-color: ", ";\n  }\n"])), function (p) { return p.theme.fontSizeMedium; }, space_1.default(2), space_1.default(0.5), space_1.default(1), function (p) { return p.theme.rowBackground; });
var StyledVersion = styled_1.default(version_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  ", "\n  line-height: 1.6;\n"], ["\n  ", "\n  line-height: 1.6;\n"])), overflowEllipsis_1.default);
var StyledEmptyStateWarning = styled_1.default(emptyStateWarning_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  height: ", ";\n  justify-content: center;\n"], ["\n  height: ", ";\n  justify-content: center;\n"])), PLACEHOLDER_AND_EMPTY_HEIGHT);
exports.default = ProjectLatestReleases;
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=projectLatestReleases.jsx.map
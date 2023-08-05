Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var Sentry = tslib_1.__importStar(require("@sentry/react"));
var indicator_1 = require("app/actionCreators/indicator");
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var thirds_1 = require("app/components/layouts/thirds");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var panels_1 = require("app/components/panels");
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var withRepositories_1 = tslib_1.__importDefault(require("app/utils/withRepositories"));
var emptyMessage_1 = tslib_1.__importDefault(require("app/views/settings/components/emptyMessage"));
var _1 = require(".");
function withReleaseRepos(WrappedComponent) {
    var WithReleaseRepos = /** @class */ (function (_super) {
        tslib_1.__extends(WithReleaseRepos, _super);
        function WithReleaseRepos() {
            var _this = _super !== null && _super.apply(this, arguments) || this;
            _this.state = {
                releaseRepos: [],
                isLoading: true,
            };
            return _this;
        }
        WithReleaseRepos.prototype.componentDidMount = function () {
            this.fetchReleaseRepos();
        };
        WithReleaseRepos.prototype.UNSAFE_componentWillReceiveProps = function (nextProps) {
            this.setActiveReleaseRepo(nextProps);
        };
        WithReleaseRepos.prototype.componentDidUpdate = function (prevProps, prevState) {
            if (this.props.params.release !== prevProps.params.release ||
                (!!prevProps.repositoriesLoading && !this.props.repositoriesLoading)) {
                this.fetchReleaseRepos();
                return;
            }
            if (prevState.releaseRepos.length !== this.state.releaseRepos.length) {
                this.setActiveReleaseRepo(this.props);
            }
        };
        WithReleaseRepos.prototype.setActiveReleaseRepo = function (props) {
            var _a, _b;
            var _c = this.state, releaseRepos = _c.releaseRepos, activeReleaseRepo = _c.activeReleaseRepo;
            if (!releaseRepos.length) {
                return;
            }
            var activeCommitRepo = (_a = props.location.query) === null || _a === void 0 ? void 0 : _a.activeRepo;
            if (!activeCommitRepo) {
                this.setState({
                    activeReleaseRepo: (_b = releaseRepos[0]) !== null && _b !== void 0 ? _b : null,
                });
                return;
            }
            if (activeCommitRepo === (activeReleaseRepo === null || activeReleaseRepo === void 0 ? void 0 : activeReleaseRepo.name)) {
                return;
            }
            var matchedRepository = releaseRepos.find(function (commitRepo) { return commitRepo.name === activeCommitRepo; });
            if (matchedRepository) {
                this.setState({
                    activeReleaseRepo: matchedRepository,
                });
                return;
            }
            indicator_1.addErrorMessage(locale_1.t('The repository you were looking for was not found.'));
        };
        WithReleaseRepos.prototype.fetchReleaseRepos = function () {
            return tslib_1.__awaiter(this, void 0, void 0, function () {
                var _a, params, api, repositories, repositoriesLoading, release, orgId, project, releasePath, releaseRepos, error_1;
                return tslib_1.__generator(this, function (_b) {
                    switch (_b.label) {
                        case 0:
                            _a = this.props, params = _a.params, api = _a.api, repositories = _a.repositories, repositoriesLoading = _a.repositoriesLoading;
                            if (repositoriesLoading === undefined || repositoriesLoading === true) {
                                return [2 /*return*/];
                            }
                            if (!(repositories === null || repositories === void 0 ? void 0 : repositories.length)) {
                                this.setState({ isLoading: false });
                                return [2 /*return*/];
                            }
                            release = params.release, orgId = params.orgId;
                            project = this.context.project;
                            this.setState({ isLoading: true });
                            _b.label = 1;
                        case 1:
                            _b.trys.push([1, 3, , 4]);
                            releasePath = encodeURIComponent(release);
                            return [4 /*yield*/, api.requestPromise("/projects/" + orgId + "/" + project.slug + "/releases/" + releasePath + "/repositories/")];
                        case 2:
                            releaseRepos = _b.sent();
                            this.setState({ releaseRepos: releaseRepos, isLoading: false });
                            this.setActiveReleaseRepo(this.props);
                            return [3 /*break*/, 4];
                        case 3:
                            error_1 = _b.sent();
                            Sentry.captureException(error_1);
                            indicator_1.addErrorMessage(locale_1.t('An error occured while trying to fetch the repositories of the release: %s', release));
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        WithReleaseRepos.prototype.render = function () {
            var _a = this.state, isLoading = _a.isLoading, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos;
            var _b = this.props, repositoriesLoading = _b.repositoriesLoading, repositories = _b.repositories, params = _b.params, router = _b.router, location = _b.location, organization = _b.organization;
            if (isLoading || repositoriesLoading) {
                return <loadingIndicator_1.default />;
            }
            var noRepositoryOrgRelatedFound = !(repositories === null || repositories === void 0 ? void 0 : repositories.length);
            if (noRepositoryOrgRelatedFound) {
                var orgId = params.orgId;
                return (<thirds_1.Body>
            <thirds_1.Main fullWidth>
              <panels_1.Panel dashedBorder>
                <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={locale_1.t('Releases are better with commit data!')} description={locale_1.t('Connect a repository to see commit info, files changed, and authors involved in future releases.')} action={<button_1.default priority="primary" to={"/settings/" + orgId + "/repos/"}>
                      {locale_1.t('Connect a repository')}
                    </button_1.default>}/>
              </panels_1.Panel>
            </thirds_1.Main>
          </thirds_1.Body>);
            }
            var noReleaseReposFound = !releaseRepos.length;
            if (noReleaseReposFound) {
                return (<thirds_1.Body>
            <thirds_1.Main fullWidth>
              <panels_1.Panel dashedBorder>
                <emptyMessage_1.default icon={<icons_1.IconCommit size="xl"/>} title={locale_1.t('Releases are better with commit data!')} description={locale_1.t('No commits associated with this release have been found.')}/>
              </panels_1.Panel>
            </thirds_1.Main>
          </thirds_1.Body>);
            }
            if (activeReleaseRepo === undefined) {
                return <loadingIndicator_1.default />;
            }
            var release = params.release;
            var orgSlug = organization.slug;
            return (<WrappedComponent {...this.props} orgSlug={orgSlug} projectSlug={this.context.project.slug} release={release} router={router} location={location} releaseRepos={releaseRepos} activeReleaseRepo={activeReleaseRepo}/>);
        };
        WithReleaseRepos.displayName = "withReleaseRepos(" + getDisplayName_1.default(WrappedComponent) + ")";
        WithReleaseRepos.contextType = _1.ReleaseContext;
        return WithReleaseRepos;
    }(React.Component));
    return withApi_1.default(withOrganization_1.default(withRepositories_1.default(WithReleaseRepos)));
}
exports.default = withReleaseRepos;
//# sourceMappingURL=withReleaseRepos.jsx.map
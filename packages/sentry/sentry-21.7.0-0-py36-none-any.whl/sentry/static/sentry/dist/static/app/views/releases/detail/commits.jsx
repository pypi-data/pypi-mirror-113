Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var commitRow_1 = tslib_1.__importDefault(require("app/components/commitRow"));
var thirds_1 = require("app/components/layouts/thirds");
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var locale_1 = require("app/locale");
var formatters_1 = require("app/utils/formatters");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var emptyState_1 = tslib_1.__importDefault(require("./emptyState"));
var repositorySwitcher_1 = tslib_1.__importDefault(require("./repositorySwitcher"));
var utils_1 = require("./utils");
var withReleaseRepos_1 = tslib_1.__importDefault(require("./withReleaseRepos"));
var Commits = /** @class */ (function (_super) {
    tslib_1.__extends(Commits, _super);
    function Commits() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    Commits.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, projectSlug = _a.projectSlug;
        var orgId = params.orgId;
        return routeTitle_1.default(locale_1.t('Commits - Release %s', formatters_1.formatVersion(params.release)), orgId, false, projectSlug);
    };
    Commits.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { commits: [] });
    };
    Commits.prototype.componentDidUpdate = function (prevProps, prevContext) {
        var _a, _b;
        if (((_a = prevProps.activeReleaseRepo) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = this.props.activeReleaseRepo) === null || _b === void 0 ? void 0 : _b.name)) {
            this.remountComponent();
            return;
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
    };
    Commits.prototype.getEndpoints = function () {
        var _a = this.props, projectSlug = _a.projectSlug, activeRepository = _a.activeReleaseRepo, location = _a.location, orgSlug = _a.orgSlug, release = _a.release;
        var query = utils_1.getQuery({ location: location, activeRepository: activeRepository });
        return [
            [
                'commits',
                "/projects/" + orgSlug + "/" + projectSlug + "/releases/" + encodeURIComponent(release) + "/commits/",
                { query: query },
            ],
        ];
    };
    Commits.prototype.renderLoading = function () {
        return this.renderBody();
    };
    Commits.prototype.renderContent = function () {
        var _a = this.state, commits = _a.commits, commitsPageLinks = _a.commitsPageLinks, loading = _a.loading;
        var activeReleaseRepo = this.props.activeReleaseRepo;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!commits.length) {
            return (<emptyState_1.default>
          {!activeReleaseRepo
                    ? locale_1.t('There are no commits associated with this release.')
                    : locale_1.t('There are no commits associated with this release in the %s repository.', activeReleaseRepo.name)}
        </emptyState_1.default>);
        }
        var commitsByRepository = utils_1.getCommitsByRepository(commits);
        var reposToRender = utils_1.getReposToRender(Object.keys(commitsByRepository));
        return (<react_1.Fragment>
        {reposToRender.map(function (repoName) {
                var _a;
                return (<panels_1.Panel key={repoName}>
            <panels_1.PanelHeader>{repoName}</panels_1.PanelHeader>
            <panels_1.PanelBody>
              {(_a = commitsByRepository[repoName]) === null || _a === void 0 ? void 0 : _a.map(function (commit) { return (<commitRow_1.default key={commit.id} commit={commit}/>); })}
            </panels_1.PanelBody>
          </panels_1.Panel>);
            })}
        <pagination_1.default pageLinks={commitsPageLinks}/>
      </react_1.Fragment>);
    };
    Commits.prototype.renderBody = function () {
        var _a = this.props, location = _a.location, router = _a.router, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos;
        return (<react_1.Fragment>
        {releaseRepos.length > 1 && (<repositorySwitcher_1.default repositories={releaseRepos} activeRepository={activeReleaseRepo} location={location} router={router}/>)}
        {this.renderContent()}
      </react_1.Fragment>);
    };
    Commits.prototype.renderComponent = function () {
        return (<thirds_1.Body>
        <thirds_1.Main fullWidth>{_super.prototype.renderComponent.call(this)}</thirds_1.Main>
      </thirds_1.Body>);
    };
    return Commits;
}(asyncView_1.default));
exports.default = withReleaseRepos_1.default(Commits);
//# sourceMappingURL=commits.jsx.map
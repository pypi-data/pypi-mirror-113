Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var fileChange_1 = tslib_1.__importDefault(require("app/components/fileChange"));
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
var FilesChanged = /** @class */ (function (_super) {
    tslib_1.__extends(FilesChanged, _super);
    function FilesChanged() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    FilesChanged.prototype.getTitle = function () {
        var _a = this.props, params = _a.params, projectSlug = _a.projectSlug;
        var orgId = params.orgId;
        return routeTitle_1.default(locale_1.t('Files Changed - Release %s', formatters_1.formatVersion(params.release)), orgId, false, projectSlug);
    };
    FilesChanged.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { fileList: [] });
    };
    FilesChanged.prototype.componentDidUpdate = function (prevProps, prevContext) {
        var _a, _b;
        if (((_a = prevProps.activeReleaseRepo) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = this.props.activeReleaseRepo) === null || _b === void 0 ? void 0 : _b.name)) {
            this.remountComponent();
            return;
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevContext);
    };
    FilesChanged.prototype.getEndpoints = function () {
        var _a = this.props, activeRepository = _a.activeReleaseRepo, location = _a.location, release = _a.release, orgSlug = _a.orgSlug;
        var query = utils_1.getQuery({ location: location, activeRepository: activeRepository });
        return [
            [
                'fileList',
                "/organizations/" + orgSlug + "/releases/" + encodeURIComponent(release) + "/commitfiles/",
                { query: query },
            ],
        ];
    };
    FilesChanged.prototype.renderLoading = function () {
        return this.renderBody();
    };
    FilesChanged.prototype.renderContent = function () {
        var _a = this.state, fileList = _a.fileList, fileListPageLinks = _a.fileListPageLinks, loading = _a.loading;
        var activeReleaseRepo = this.props.activeReleaseRepo;
        if (loading) {
            return <loadingIndicator_1.default />;
        }
        if (!fileList.length) {
            return (<emptyState_1.default>
          {!activeReleaseRepo
                    ? locale_1.t('There are no changed files associated with this release.')
                    : locale_1.t('There are no changed files associated with this release in the %s repository.', activeReleaseRepo.name)}
        </emptyState_1.default>);
        }
        var filesByRepository = utils_1.getFilesByRepository(fileList);
        var reposToRender = utils_1.getReposToRender(Object.keys(filesByRepository));
        return (<react_1.Fragment>
        {reposToRender.map(function (repoName) {
                var repoData = filesByRepository[repoName];
                var files = Object.keys(repoData);
                var fileCount = files.length;
                return (<panels_1.Panel key={repoName}>
              <panels_1.PanelHeader>
                <span>{repoName}</span>
                <span>{locale_1.tn('%s file changed', '%s files changed', fileCount)}</span>
              </panels_1.PanelHeader>
              <panels_1.PanelBody>
                {files.map(function (filename) {
                        var authors = repoData[filename].authors;
                        return (<StyledFileChange key={filename} filename={filename} authors={Object.values(authors)}/>);
                    })}
              </panels_1.PanelBody>
            </panels_1.Panel>);
            })}
        <pagination_1.default pageLinks={fileListPageLinks}/>
      </react_1.Fragment>);
    };
    FilesChanged.prototype.renderBody = function () {
        var _a = this.props, activeReleaseRepo = _a.activeReleaseRepo, releaseRepos = _a.releaseRepos, router = _a.router, location = _a.location;
        return (<react_1.Fragment>
        {releaseRepos.length > 1 && (<repositorySwitcher_1.default repositories={releaseRepos} activeRepository={activeReleaseRepo} location={location} router={router}/>)}
        {this.renderContent()}
      </react_1.Fragment>);
    };
    FilesChanged.prototype.renderComponent = function () {
        return (<thirds_1.Body>
        <thirds_1.Main fullWidth>{_super.prototype.renderComponent.call(this)}</thirds_1.Main>
      </thirds_1.Body>);
    };
    return FilesChanged;
}(asyncView_1.default));
exports.default = withReleaseRepos_1.default(FilesChanged);
var StyledFileChange = styled_1.default(fileChange_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"], ["\n  border-radius: 0;\n  border-left: none;\n  border-right: none;\n  border-top: none;\n  :last-child {\n    border: none;\n    border-radius: 0;\n  }\n"])));
var templateObject_1;
//# sourceMappingURL=filesChanged.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var queryString_1 = require("app/utils/queryString");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var sourceMapsArchiveRow_1 = tslib_1.__importDefault(require("./sourceMapsArchiveRow"));
var ProjectSourceMaps = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectSourceMaps, _super);
    function ProjectSourceMaps() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleDelete = function (name) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        indicator_1.addLoadingMessage(locale_1.t('Removing artifacts\u2026'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise(this.getArchivesUrl(), {
                                method: 'DELETE',
                                query: { name: name },
                            })];
                    case 2:
                        _b.sent();
                        this.fetchData();
                        indicator_1.addSuccessMessage(locale_1.t('Artifacts removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to remove artifacts. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectSourceMaps.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Source Maps'), projectId, false);
    };
    ProjectSourceMaps.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { archives: [] });
    };
    ProjectSourceMaps.prototype.getEndpoints = function () {
        return [['archives', this.getArchivesUrl(), { query: { query: this.getQuery() } }]];
    };
    ProjectSourceMaps.prototype.getArchivesUrl = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId;
        return "/projects/" + orgId + "/" + projectId + "/files/source-maps/";
    };
    ProjectSourceMaps.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return queryString_1.decodeScalar(query);
    };
    ProjectSourceMaps.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return locale_1.t('There are no archives that match your search.');
        }
        return locale_1.t('There are no archives for this project.');
    };
    ProjectSourceMaps.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectSourceMaps.prototype.renderArchives = function () {
        var _this = this;
        var archives = this.state.archives;
        var params = this.props.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!archives.length) {
            return null;
        }
        return archives.map(function (a) {
            return (<sourceMapsArchiveRow_1.default key={a.name} archive={a} orgId={orgId} projectId={projectId} onDelete={_this.handleDelete}/>);
        });
    };
    ProjectSourceMaps.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, archives = _a.archives, archivesPageLinks = _a.archivesPageLinks;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Source Maps')} action={<searchBar_1.default placeholder={locale_1.t('Filter Archives')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <textBlock_1.default>
          {locale_1.tct("These source map archives help Sentry identify where to look when Javascript is minified. By providing this information, you can get better context for your stack traces when debugging. To learn more about source maps, [link: read the docs].", {
                link: (<externalLink_1.default href="https://docs.sentry.io/platforms/javascript/sourcemaps/"/>),
            })}
        </textBlock_1.default>

        <StyledPanelTable headers={[
                locale_1.t('Archive'),
                <ArtifactsColumn key="artifacts">{locale_1.t('Artifacts')}</ArtifactsColumn>,
                locale_1.t('Type'),
                locale_1.t('Date Created'),
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={archives.length === 0} isLoading={loading}>
          {this.renderArchives()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={archivesPageLinks}/>
      </react_1.Fragment>);
    };
    return ProjectSourceMaps;
}(asyncView_1.default));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns:\n    minmax(120px, 1fr) max-content minmax(85px, max-content) minmax(265px, max-content)\n    75px;\n"], ["\n  grid-template-columns:\n    minmax(120px, 1fr) max-content minmax(85px, max-content) minmax(265px, max-content)\n    75px;\n"])));
var ArtifactsColumn = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n  padding-right: ", ";\n  margin-right: ", ";\n"], ["\n  text-align: right;\n  padding-right: ", ";\n  margin-right: ", ";\n"])), space_1.default(1.5), space_1.default(0.25));
exports.default = ProjectSourceMaps;
var templateObject_1, templateObject_2;
//# sourceMappingURL=index.jsx.map
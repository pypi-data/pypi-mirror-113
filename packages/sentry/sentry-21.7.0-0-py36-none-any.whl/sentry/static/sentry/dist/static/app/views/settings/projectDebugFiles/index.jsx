Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var checkbox_1 = tslib_1.__importDefault(require("app/components/checkbox"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var debugFileRow_1 = tslib_1.__importDefault(require("./debugFileRow"));
var externalSources_1 = tslib_1.__importDefault(require("./externalSources"));
var ProjectDebugSymbols = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectDebugSymbols, _super);
    function ProjectDebugSymbols() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (id) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + id, {
                method: 'DELETE',
                complete: function () { return _this.fetchData(); },
            });
        };
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        return _this;
    }
    ProjectDebugSymbols.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('Debug Files'), projectId, false);
    };
    ProjectDebugSymbols.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { project: this.props.project, showDetails: false });
    };
    ProjectDebugSymbols.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, params = _a.params, location = _a.location;
        var builtinSymbolSources = (this.state || {}).builtinSymbolSources;
        var orgId = params.orgId, projectId = params.projectId;
        var query = location.query.query;
        var endpoints = [
            [
                'debugFiles',
                "/projects/" + orgId + "/" + projectId + "/files/dsyms/",
                {
                    query: {
                        query: query,
                        file_formats: [
                            'breakpad',
                            'macho',
                            'elf',
                            'pe',
                            'pdb',
                            'sourcebundle',
                            'wasm',
                            'bcsymbolmap',
                            'uuidmap',
                        ],
                    },
                },
            ],
        ];
        if (!builtinSymbolSources && organization.features.includes('symbol-sources')) {
            endpoints.push(['builtinSymbolSources', '/builtin-symbol-sources/', {}]);
        }
        return endpoints;
    };
    ProjectDebugSymbols.prototype.fetchProject = function () {
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var params, orgId, projectId, updatedProject, _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        params = this.props.params;
                        orgId = params.orgId, projectId = params.projectId;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/")];
                    case 2:
                        updatedProject = _b.sent();
                        projectActions_1.default.updateSuccess(updatedProject);
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('An error occured while fetching project data'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        });
    };
    ProjectDebugSymbols.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ProjectDebugSymbols.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return locale_1.t('There are no debug symbols that match your search.');
        }
        return locale_1.t('There are no debug symbols for this project.');
    };
    ProjectDebugSymbols.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectDebugSymbols.prototype.renderDebugFiles = function () {
        var _this = this;
        var _a = this.state, debugFiles = _a.debugFiles, showDetails = _a.showDetails;
        var _b = this.props, organization = _b.organization, params = _b.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length)) {
            return null;
        }
        return debugFiles.map(function (debugFile) {
            var downloadUrl = _this.api.baseUrl + "/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + debugFile.id;
            return (<debugFileRow_1.default debugFile={debugFile} showDetails={showDetails} downloadUrl={downloadUrl} downloadRole={organization.debugFilesRole} onDelete={_this.handleDelete} key={debugFile.id}/>);
        });
    };
    ProjectDebugSymbols.prototype.renderBody = function () {
        var _this = this;
        var _a;
        var _b = this.props, organization = _b.organization, project = _b.project, router = _b.router, location = _b.location;
        var _c = this.state, loading = _c.loading, showDetails = _c.showDetails, builtinSymbolSources = _c.builtinSymbolSources, debugFiles = _c.debugFiles, debugFilesPageLinks = _c.debugFilesPageLinks;
        var features = organization.features;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('Debug Information Files')}/>

        <textBlock_1.default>
          {locale_1.t("\n            Debug information files are used to convert addresses and minified\n            function names from native crash reports into function names and\n            locations.\n          ")}
        </textBlock_1.default>

        {features.includes('symbol-sources') && (<react_1.Fragment>
            <permissionAlert_1.default />
            <externalSources_1.default api={this.api} location={location} router={router} projectSlug={project.slug} organization={organization} symbolSources={project.symbolSources ? JSON.parse(project.symbolSources) : []} builtinSymbolSources={(_a = project.builtinSymbolSources) !== null && _a !== void 0 ? _a : []} builtinSymbolSourceOptions={builtinSymbolSources !== null && builtinSymbolSources !== void 0 ? builtinSymbolSources : []}/>
          </react_1.Fragment>)}

        <Wrapper>
          <textBlock_1.default noMargin>{locale_1.t('Uploaded debug information files')}:</textBlock_1.default>

          <Filters>
            <Label>
              <checkbox_1.default checked={showDetails} onChange={function (e) {
                _this.setState({ showDetails: e.target.checked });
            }}/>
              {locale_1.t('show details')}
            </Label>

            <searchBar_1.default placeholder={locale_1.t('Search DIFs')} onSearch={this.handleSearch} query={this.getQuery()}/>
          </Filters>
        </Wrapper>

        <StyledPanelTable headers={[
                locale_1.t('Debug ID'),
                locale_1.t('Information'),
                <Actions key="actions">{locale_1.t('Actions')}</Actions>,
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={(debugFiles === null || debugFiles === void 0 ? void 0 : debugFiles.length) === 0} isLoading={loading}>
          {this.renderDebugFiles()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={debugFilesPageLinks}/>
      </react_1.Fragment>);
    };
    return ProjectDebugSymbols;
}(asyncView_1.default));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: 37% 1fr auto;\n"], ["\n  grid-template-columns: 37% 1fr auto;\n"])));
var Actions = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
var Wrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: auto 1fr;\n  grid-gap: ", ";\n  align-items: center;\n  margin-top: ", ";\n  margin-bottom: ", ";\n  @media (max-width: ", ") {\n    display: block;\n  }\n"])), space_1.default(4), space_1.default(4), space_1.default(1), function (p) { return p.theme.breakpoints[0]; });
var Filters = styled_1.default('div')(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"], ["\n  display: grid;\n  grid-template-columns: min-content minmax(200px, 400px);\n  align-items: center;\n  justify-content: flex-end;\n  grid-gap: ", ";\n  @media (max-width: ", ") {\n    grid-template-columns: min-content 1fr;\n  }\n"])), space_1.default(2), function (p) { return p.theme.breakpoints[0]; });
var Label = styled_1.default('label')(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"], ["\n  font-weight: normal;\n  display: flex;\n  margin-bottom: 0;\n  white-space: nowrap;\n  input {\n    margin-top: 0;\n    margin-right: ", ";\n  }\n"])), space_1.default(1));
exports.default = ProjectDebugSymbols;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5;
//# sourceMappingURL=index.jsx.map
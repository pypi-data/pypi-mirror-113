Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var externalLink_1 = tslib_1.__importDefault(require("app/components/links/externalLink"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var locale_1 = require("app/locale");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var projectProguardRow_1 = tslib_1.__importDefault(require("./projectProguardRow"));
var ProjectProguard = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectProguard, _super);
    function ProjectProguard() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleDelete = function (id) {
            var _a = _this.props.params, orgId = _a.orgId, projectId = _a.projectId;
            _this.setState({
                loading: true,
            });
            _this.api.request("/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(id), {
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
    ProjectProguard.prototype.getTitle = function () {
        var projectId = this.props.params.projectId;
        return routeTitle_1.default(locale_1.t('ProGuard Mappings'), projectId, false);
    };
    ProjectProguard.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { mappings: [] });
    };
    ProjectProguard.prototype.getEndpoints = function () {
        var _a = this.props, params = _a.params, location = _a.location;
        var orgId = params.orgId, projectId = params.projectId;
        var endpoints = [
            [
                'mappings',
                "/projects/" + orgId + "/" + projectId + "/files/dsyms/",
                { query: { query: location.query.query, file_formats: 'proguard' } },
            ],
        ];
        return endpoints;
    };
    ProjectProguard.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return typeof query === 'string' ? query : undefined;
    };
    ProjectProguard.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return locale_1.t('There are no mappings that match your search.');
        }
        return locale_1.t('There are no mappings for this project.');
    };
    ProjectProguard.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectProguard.prototype.renderMappings = function () {
        var _this = this;
        var mappings = this.state.mappings;
        var _a = this.props, organization = _a.organization, params = _a.params;
        var orgId = params.orgId, projectId = params.projectId;
        if (!(mappings === null || mappings === void 0 ? void 0 : mappings.length)) {
            return null;
        }
        return mappings.map(function (mapping) {
            var downloadUrl = _this.api.baseUrl + "/projects/" + orgId + "/" + projectId + "/files/dsyms/?id=" + encodeURIComponent(mapping.id);
            return (<projectProguardRow_1.default mapping={mapping} downloadUrl={downloadUrl} onDelete={_this.handleDelete} downloadRole={organization.debugFilesRole} key={mapping.id}/>);
        });
    };
    ProjectProguard.prototype.renderBody = function () {
        var _a = this.state, loading = _a.loading, mappings = _a.mappings, mappingsPageLinks = _a.mappingsPageLinks;
        return (<react_1.Fragment>
        <settingsPageHeader_1.default title={locale_1.t('ProGuard Mappings')} action={<searchBar_1.default placeholder={locale_1.t('Filter mappings')} onSearch={this.handleSearch} query={this.getQuery()} width="280px"/>}/>

        <textBlock_1.default>
          {locale_1.tct("ProGuard mapping files are used to convert minified classes, methods and field names into a human readable format. To learn more about proguard mapping files, [link: read the docs].", {
                link: (<externalLink_1.default href="https://docs.sentry.io/platforms/android/proguard/"/>),
            })}
        </textBlock_1.default>

        <StyledPanelTable headers={[
                locale_1.t('Mapping'),
                <SizeColumn key="size">{locale_1.t('File Size')}</SizeColumn>,
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={(mappings === null || mappings === void 0 ? void 0 : mappings.length) === 0} isLoading={loading}>
          {this.renderMappings()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={mappingsPageLinks}/>
      </react_1.Fragment>);
    };
    return ProjectProguard;
}(asyncView_1.default));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"], ["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"])));
var SizeColumn = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
exports.default = ProjectProguard;
var templateObject_1, templateObject_2;
//# sourceMappingURL=projectProguard.jsx.map
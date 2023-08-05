Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var indicator_1 = require("app/actionCreators/indicator");
var access_1 = tslib_1.__importDefault(require("app/components/acl/access"));
var button_1 = tslib_1.__importDefault(require("app/components/button"));
var buttonBar_1 = tslib_1.__importDefault(require("app/components/buttonBar"));
var confirm_1 = tslib_1.__importDefault(require("app/components/confirm"));
var pagination_1 = tslib_1.__importDefault(require("app/components/pagination"));
var panels_1 = require("app/components/panels");
var searchBar_1 = tslib_1.__importDefault(require("app/components/searchBar"));
var textOverflow_1 = tslib_1.__importDefault(require("app/components/textOverflow"));
var tooltip_1 = tslib_1.__importDefault(require("app/components/tooltip"));
var version_1 = tslib_1.__importDefault(require("app/components/version"));
var icons_1 = require("app/icons");
var locale_1 = require("app/locale");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var formatters_1 = require("app/utils/formatters");
var queryString_1 = require("app/utils/queryString");
var routeTitle_1 = tslib_1.__importDefault(require("app/utils/routeTitle"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var sourceMapsArtifactRow_1 = tslib_1.__importDefault(require("./sourceMapsArtifactRow"));
var ProjectSourceMapsDetail = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectSourceMapsDetail, _super);
    function ProjectSourceMapsDetail() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleSearch = function (query) {
            var _a = _this.props, location = _a.location, router = _a.router;
            router.push(tslib_1.__assign(tslib_1.__assign({}, location), { query: tslib_1.__assign(tslib_1.__assign({}, location.query), { cursor: undefined, query: query }) }));
        };
        _this.handleArtifactDelete = function (id) { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        indicator_1.addLoadingMessage(locale_1.t('Removing artifact\u2026'));
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("" + this.getArtifactsUrl() + id + "/", {
                                method: 'DELETE',
                            })];
                    case 2:
                        _b.sent();
                        this.fetchData();
                        indicator_1.addSuccessMessage(locale_1.t('Artifact removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _a = _b.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to remove artifact. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        _this.handleArchiveDelete = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, orgId, projectId, name, _b;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, name = _a.name;
                        indicator_1.addLoadingMessage(locale_1.t('Removing artifacts\u2026'));
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, this.api.requestPromise("/projects/" + orgId + "/" + projectId + "/files/source-maps/", {
                                method: 'DELETE',
                                query: { name: name },
                            })];
                    case 2:
                        _c.sent();
                        this.fetchData();
                        indicator_1.addSuccessMessage(locale_1.t('Artifacts removed.'));
                        return [3 /*break*/, 4];
                    case 3:
                        _b = _c.sent();
                        indicator_1.addErrorMessage(locale_1.t('Unable to remove artifacts. Please try again.'));
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        return _this;
    }
    ProjectSourceMapsDetail.prototype.getTitle = function () {
        var _a = this.props.params, projectId = _a.projectId, name = _a.name;
        return routeTitle_1.default(locale_1.t('Archive %s', formatters_1.formatVersion(name)), projectId, false);
    };
    ProjectSourceMapsDetail.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { artifacts: [] });
    };
    ProjectSourceMapsDetail.prototype.getEndpoints = function () {
        return [['artifacts', this.getArtifactsUrl(), { query: { query: this.getQuery() } }]];
    };
    ProjectSourceMapsDetail.prototype.getArtifactsUrl = function () {
        var _a = this.props.params, orgId = _a.orgId, projectId = _a.projectId, name = _a.name;
        return "/projects/" + orgId + "/" + projectId + "/releases/" + encodeURIComponent(name) + "/files/";
    };
    ProjectSourceMapsDetail.prototype.getQuery = function () {
        var query = this.props.location.query.query;
        return queryString_1.decodeScalar(query);
    };
    ProjectSourceMapsDetail.prototype.getEmptyMessage = function () {
        if (this.getQuery()) {
            return locale_1.t('There are no artifacts that match your search.');
        }
        return locale_1.t('There are no artifacts in this archive.');
    };
    ProjectSourceMapsDetail.prototype.renderLoading = function () {
        return this.renderBody();
    };
    ProjectSourceMapsDetail.prototype.renderArtifacts = function () {
        var _this = this;
        var organization = this.props.organization;
        var artifacts = this.state.artifacts;
        var artifactApiUrl = this.api.baseUrl + this.getArtifactsUrl();
        if (!artifacts.length) {
            return null;
        }
        return artifacts.map(function (artifact) {
            return (<sourceMapsArtifactRow_1.default key={artifact.id} artifact={artifact} onDelete={_this.handleArtifactDelete} downloadUrl={"" + artifactApiUrl + artifact.id + "/?download=1"} downloadRole={organization.debugFilesRole}/>);
        });
    };
    ProjectSourceMapsDetail.prototype.renderBody = function () {
        var _this = this;
        var _a = this.state, loading = _a.loading, artifacts = _a.artifacts, artifactsPageLinks = _a.artifactsPageLinks;
        var _b = this.props.params, name = _b.name, orgId = _b.orgId;
        var project = this.props.project;
        return (<react_1.Fragment>
        <StyledSettingsPageHeader title={<Title>
              {locale_1.t('Archive')}&nbsp;
              <textOverflow_1.default>
                <version_1.default version={name} tooltipRawVersion anchor={false} truncate/>
              </textOverflow_1.default>
            </Title>} action={<StyledButtonBar gap={1}>
              <ReleaseButton to={"/organizations/" + orgId + "/releases/" + encodeURIComponent(name) + "/?project=" + project.id}>
                {locale_1.t('Go to Release')}
              </ReleaseButton>
              <access_1.default access={['project:releases']}>
                {function (_a) {
                    var hasAccess = _a.hasAccess;
                    return (<tooltip_1.default disabled={hasAccess} title={locale_1.t('You do not have permission to delete artifacts.')}>
                    <confirm_1.default message={locale_1.t('Are you sure you want to remove all artifacts in this archive?')} onConfirm={_this.handleArchiveDelete} disabled={!hasAccess}>
                      <button_1.default icon={<icons_1.IconDelete size="sm"/>} title={locale_1.t('Remove All Artifacts')} label={locale_1.t('Remove All Artifacts')} disabled={!hasAccess}/>
                    </confirm_1.default>
                  </tooltip_1.default>);
                }}
              </access_1.default>

              <searchBar_1.default placeholder={locale_1.t('Filter artifacts')} onSearch={this.handleSearch} query={this.getQuery()}/>
            </StyledButtonBar>}/>

        <StyledPanelTable headers={[
                locale_1.t('Artifact'),
                <SizeColumn key="size">{locale_1.t('File Size')}</SizeColumn>,
                '',
            ]} emptyMessage={this.getEmptyMessage()} isEmpty={artifacts.length === 0} isLoading={loading}>
          {this.renderArtifacts()}
        </StyledPanelTable>
        <pagination_1.default pageLinks={artifactsPageLinks}/>
      </react_1.Fragment>);
    };
    return ProjectSourceMapsDetail;
}(asyncView_1.default));
var StyledSettingsPageHeader = styled_1.default(settingsPageHeader_1.default)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  /*\n    ugly selector to make header work on mobile\n    we can refactor this once we start making other settings more responsive\n  */\n  > div {\n    @media (max-width: ", ") {\n      display: block;\n    }\n    > div {\n      min-width: 0;\n      @media (max-width: ", ") {\n        margin-bottom: ", ";\n      }\n    }\n  }\n"], ["\n  /*\n    ugly selector to make header work on mobile\n    we can refactor this once we start making other settings more responsive\n  */\n  > div {\n    @media (max-width: ", ") {\n      display: block;\n    }\n    > div {\n      min-width: 0;\n      @media (max-width: ", ") {\n        margin-bottom: ", ";\n      }\n    }\n  }\n"])), function (p) { return p.theme.breakpoints[2]; }, function (p) { return p.theme.breakpoints[2]; }, space_1.default(2));
var Title = styled_1.default('div')(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  display: flex;\n  align-items: center;\n"], ["\n  display: flex;\n  align-items: center;\n"])));
var StyledButtonBar = styled_1.default(buttonBar_1.default)(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  justify-content: flex-start;\n"], ["\n  justify-content: flex-start;\n"])));
var StyledPanelTable = styled_1.default(panels_1.PanelTable)(templateObject_4 || (templateObject_4 = tslib_1.__makeTemplateObject(["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"], ["\n  grid-template-columns: minmax(220px, 1fr) max-content 120px;\n"])));
var ReleaseButton = styled_1.default(button_1.default)(templateObject_5 || (templateObject_5 = tslib_1.__makeTemplateObject(["\n  white-space: nowrap;\n"], ["\n  white-space: nowrap;\n"])));
var SizeColumn = styled_1.default('div')(templateObject_6 || (templateObject_6 = tslib_1.__makeTemplateObject(["\n  text-align: right;\n"], ["\n  text-align: right;\n"])));
exports.default = ProjectSourceMapsDetail;
var templateObject_1, templateObject_2, templateObject_3, templateObject_4, templateObject_5, templateObject_6;
//# sourceMappingURL=index.jsx.map
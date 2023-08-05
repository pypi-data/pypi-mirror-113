Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_select_1 = require("react-select");
var react_1 = require("@emotion/react");
var styled_1 = tslib_1.__importDefault(require("@emotion/styled"));
var cloneDeep_1 = tslib_1.__importDefault(require("lodash/cloneDeep"));
var set_1 = tslib_1.__importDefault(require("lodash/set"));
var projectBadge_1 = tslib_1.__importDefault(require("app/components/idBadge/projectBadge"));
var Layout = tslib_1.__importStar(require("app/components/layouts/thirds"));
var pickProjectToContinue_1 = tslib_1.__importDefault(require("app/components/pickProjectToContinue"));
var locale_1 = require("app/locale");
var organization_1 = require("app/styles/organization");
var space_1 = tslib_1.__importDefault(require("app/styles/space"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
var asyncView_1 = tslib_1.__importDefault(require("app/views/asyncView"));
var selectField_1 = tslib_1.__importDefault(require("app/views/settings/components/forms/selectField"));
var buildStep_1 = tslib_1.__importDefault(require("../buildStep"));
var buildSteps_1 = tslib_1.__importDefault(require("../buildSteps"));
var choseDataStep_1 = tslib_1.__importDefault(require("../choseDataStep"));
var header_1 = tslib_1.__importDefault(require("../header"));
var utils_1 = require("../utils");
var card_1 = tslib_1.__importDefault(require("./card"));
var queries_1 = tslib_1.__importDefault(require("./queries"));
var searchQueryField_1 = tslib_1.__importDefault(require("./searchQueryField"));
var MetricWidget = /** @class */ (function (_super) {
    tslib_1.__extends(MetricWidget, _super);
    function MetricWidget() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.handleFieldChange = function (field, value) {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                if (field === 'displayType') {
                    if (state.title === locale_1.t('Custom %s Widget', state.displayType) ||
                        state.title === locale_1.t('Custom %s Widget', utils_1.DisplayType.AREA)) {
                        return tslib_1.__assign(tslib_1.__assign({}, newState), { title: locale_1.t('Custom %s Widget', utils_1.displayTypes[value]), widgetErrors: undefined });
                    }
                    set_1.default(newState, field, value);
                }
                return tslib_1.__assign(tslib_1.__assign({}, newState), { widgetErrors: undefined });
            });
        };
        _this.handleRemoveQuery = function (index) {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                newState.queries.splice(index, 1);
                return newState;
            });
        };
        _this.handleAddQuery = function () {
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                newState.queries.push({});
                return newState;
            });
        };
        _this.handleChangeQuery = function (index, query) {
            var _a, _b;
            var isMetricNew = ((_a = _this.state.queries[index].metricMeta) === null || _a === void 0 ? void 0 : _a.name) !== ((_b = query.metricMeta) === null || _b === void 0 ? void 0 : _b.name);
            if (isMetricNew) {
                query.aggregation = query.metricMeta ? query.metricMeta.operations[0] : undefined;
            }
            _this.setState(function (state) {
                var newState = cloneDeep_1.default(state);
                set_1.default(newState, "queries." + index, query);
                return newState;
            });
        };
        _this.handleProjectChange = function (projectId) {
            var _a = _this.props, router = _a.router, location = _a.location;
            // if we change project, we need to sync the project slug in the URL
            router.replace({
                pathname: location.pathname,
                query: tslib_1.__assign(tslib_1.__assign({}, location.query), { project: projectId }),
            });
        };
        return _this;
    }
    MetricWidget.prototype.getDefaultState = function () {
        return tslib_1.__assign(tslib_1.__assign({}, _super.prototype.getDefaultState.call(this)), { title: locale_1.t('Custom %s Widget', utils_1.displayTypes[utils_1.DisplayType.AREA]), displayType: utils_1.DisplayType.AREA, metricMetas: [], metricTags: [], queries: [{}] });
    };
    Object.defineProperty(MetricWidget.prototype, "project", {
        get: function () {
            var _a = this.props, projects = _a.projects, location = _a.location;
            var query = location.query;
            var projectId = query.project;
            return projects.find(function (project) { return project.id === projectId; });
        },
        enumerable: false,
        configurable: true
    });
    MetricWidget.prototype.getEndpoints = function () {
        var _a = this.props, organization = _a.organization, loadingProjects = _a.loadingProjects;
        if (this.isProjectMissingInUrl() || loadingProjects || !this.project) {
            return [];
        }
        var orgSlug = organization.slug;
        var projectSlug = this.project.slug;
        return [
            ['metricMetas', "/projects/" + orgSlug + "/" + projectSlug + "/metrics/meta/"],
            ['metricTags', "/projects/" + orgSlug + "/" + projectSlug + "/metrics/tags/"],
        ];
    };
    MetricWidget.prototype.componentDidUpdate = function (prevProps, prevState) {
        var _a, _b;
        if (prevProps.loadingProjects && !this.props.loadingProjects) {
            this.reloadData();
        }
        if (!((_a = prevState.metricMetas) === null || _a === void 0 ? void 0 : _a.length) && !!((_b = this.state.metricMetas) === null || _b === void 0 ? void 0 : _b.length)) {
            this.handleChangeQuery(0, { metricMeta: this.state.metricMetas[0] });
        }
        _super.prototype.componentDidUpdate.call(this, prevProps, prevState);
    };
    MetricWidget.prototype.isProjectMissingInUrl = function () {
        var projectId = this.props.location.query.project;
        return !projectId || typeof projectId !== 'string';
    };
    MetricWidget.prototype.renderBody = function () {
        var _this = this;
        var _a = this.props, organization = _a.organization, router = _a.router, projects = _a.projects, onChangeDataSet = _a.onChangeDataSet, selection = _a.selection, location = _a.location, loadingProjects = _a.loadingProjects, goBackLocation = _a.goBackLocation, dashboardTitle = _a.dashboardTitle;
        var _b = this.state, title = _b.title, metricTags = _b.metricTags, searchQuery = _b.searchQuery, metricMetas = _b.metricMetas, queries = _b.queries, displayType = _b.displayType;
        var orgSlug = organization.slug;
        if (loadingProjects) {
            return this.renderLoading();
        }
        var selectedProject = this.project;
        if (this.isProjectMissingInUrl() || !selectedProject) {
            return (<pickProjectToContinue_1.default router={router} projects={projects.map(function (project) { return ({ id: project.id, slug: project.slug }); })} nextPath={{
                    pathname: location.pathname,
                    query: location.query,
                }} noProjectRedirectPath={goBackLocation}/>);
        }
        if (!metricTags || !metricMetas) {
            return null;
        }
        return (<StyledPageContent>
        <header_1.default orgSlug={orgSlug} title={title} dashboardTitle={dashboardTitle} goBackLocation={goBackLocation} onChangeTitle={function (newTitle) { return _this.handleFieldChange('title', newTitle); }}/>
        <Layout.Body>
          <buildSteps_1.default>
            <buildStep_1.default title={locale_1.t('Choose your visualization')} description={locale_1.t('This is a preview of how your widget will appear in the dashboard.')}>
              <VisualizationWrapper>
                <StyledSelectField name="displayType" choices={[utils_1.DisplayType.LINE, utils_1.DisplayType.BAR, utils_1.DisplayType.AREA].map(function (value) { return [value, utils_1.displayTypes[value]]; })} value={displayType} onChange={function (value) {
                _this.handleFieldChange('displayType', value);
            }} inline={false} flexibleControlStateSize stacked/>
                <card_1.default router={router} location={location} selection={selection} organization={organization} api={this.api} project={selectedProject} widget={{
                title: title,
                searchQuery: searchQuery,
                displayType: displayType,
                groupings: queries,
            }}/>
              </VisualizationWrapper>
            </buildStep_1.default>
            <choseDataStep_1.default value={utils_1.DataSet.METRICS} onChange={onChangeDataSet}/>
            <buildStep_1.default title={locale_1.t('Choose your project')} description={locale_1.t('You’ll need to select a project to set metrics on.')}>
              <StyledSelectField name="project" choices={projects.map(function (project) { return [project, project.slug]; })} onChange={function (project) { return _this.handleProjectChange(project.id); }} value={selectedProject} components={{
                Option: function (_a) {
                    var label = _a.label, optionProps = tslib_1.__rest(_a, ["label"]);
                    var data = optionProps.data;
                    return (<react_select_1.components.Option label={label} {...optionProps}>
                        <projectBadge_1.default project={data.value} avatarSize={18} disableLink/>
                      </react_select_1.components.Option>);
                },
                SingleValue: function (_a) {
                    var data = _a.data, props = tslib_1.__rest(_a, ["data"]);
                    return (<react_select_1.components.SingleValue data={data} {...props}>
                      <projectBadge_1.default project={data.value} avatarSize={18} disableLink/>
                    </react_select_1.components.SingleValue>);
                },
            }} styles={{
                control: function (provided) { return (tslib_1.__assign(tslib_1.__assign({}, provided), { boxShadow: 'none' })); },
            }} allowClear={false} inline={false} flexibleControlStateSize stacked/>
            </buildStep_1.default>
            <buildStep_1.default title={locale_1.t('Begin your search')} description={locale_1.t('Select a tag to compare releases, session data, etc.')}>
              <searchQueryField_1.default api={this.api} tags={metricTags} orgSlug={orgSlug} projectSlug={selectedProject.slug} query={searchQuery} onSearch={function (newQuery) { return _this.handleFieldChange('searchQuery', newQuery); }} onBlur={function (newQuery) { return _this.handleFieldChange('searchQuery', newQuery); }}/>
            </buildStep_1.default>
            <buildStep_1.default title={locale_1.t('Add queries')} description={locale_1.t('We’ll use this to determine what gets graphed in the y-axis and any additional overlays.')}>
              <queries_1.default metricMetas={metricMetas} metricTags={metricTags} queries={queries} onAddQuery={this.handleAddQuery} onRemoveQuery={this.handleRemoveQuery} onChangeQuery={this.handleChangeQuery}/>
            </buildStep_1.default>
          </buildSteps_1.default>
        </Layout.Body>
      </StyledPageContent>);
    };
    return MetricWidget;
}(asyncView_1.default));
exports.default = react_1.withTheme(withProjects_1.default(withGlobalSelection_1.default(MetricWidget)));
var StyledPageContent = styled_1.default(organization_1.PageContent)(templateObject_1 || (templateObject_1 = tslib_1.__makeTemplateObject(["\n  padding: 0;\n"], ["\n  padding: 0;\n"])));
var StyledSelectField = styled_1.default(selectField_1.default)(templateObject_2 || (templateObject_2 = tslib_1.__makeTemplateObject(["\n  padding-right: 0;\n"], ["\n  padding-right: 0;\n"])));
var VisualizationWrapper = styled_1.default('div')(templateObject_3 || (templateObject_3 = tslib_1.__makeTemplateObject(["\n  display: grid;\n  grid-gap: ", ";\n"], ["\n  display: grid;\n  grid-gap: ", ";\n"])), space_1.default(1.5));
var templateObject_1, templateObject_2, templateObject_3;
//# sourceMappingURL=index.jsx.map
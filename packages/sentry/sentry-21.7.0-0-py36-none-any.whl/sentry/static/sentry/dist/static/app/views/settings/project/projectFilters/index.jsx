Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var react_1 = require("react");
var react_router_1 = require("react-router");
var navTabs_1 = tslib_1.__importDefault(require("app/components/navTabs"));
var sentryDocumentTitle_1 = tslib_1.__importDefault(require("app/components/sentryDocumentTitle"));
var locale_1 = require("app/locale");
var recreateRoute_1 = tslib_1.__importDefault(require("app/utils/recreateRoute"));
var settingsPageHeader_1 = tslib_1.__importDefault(require("app/views/settings/components/settingsPageHeader"));
var textBlock_1 = tslib_1.__importDefault(require("app/views/settings/components/text/textBlock"));
var permissionAlert_1 = tslib_1.__importDefault(require("app/views/settings/project/permissionAlert"));
var groupTombstones_1 = tslib_1.__importDefault(require("app/views/settings/project/projectFilters/groupTombstones"));
var projectFiltersChart_1 = tslib_1.__importDefault(require("app/views/settings/project/projectFilters/projectFiltersChart"));
var projectFiltersSettings_1 = tslib_1.__importDefault(require("app/views/settings/project/projectFilters/projectFiltersSettings"));
var ProjectFilters = /** @class */ (function (_super) {
    tslib_1.__extends(ProjectFilters, _super);
    function ProjectFilters() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    ProjectFilters.prototype.render = function () {
        var _a = this.props, project = _a.project, params = _a.params, location = _a.location;
        var orgId = params.orgId, projectId = params.projectId, filterType = params.filterType;
        if (!project) {
            return null;
        }
        var features = new Set(project.features);
        return (<react_1.Fragment>
        <sentryDocumentTitle_1.default title={locale_1.t('Inbound Filters')} projectSlug={projectId}/>
        <settingsPageHeader_1.default title={locale_1.t('Inbound Data Filters')}/>
        <permissionAlert_1.default />

        <textBlock_1.default>
          {locale_1.t('Filters allow you to prevent Sentry from storing events in certain situations. Filtered events are tracked separately from rate limits, and do not apply to any project quotas.')}
        </textBlock_1.default>

        <div>
          <projectFiltersChart_1.default project={project} params={this.props.params}/>

          {features.has('discard-groups') && (<navTabs_1.default underlined style={{ paddingTop: '30px' }}>
              <li className={filterType === 'data-filters' ? 'active' : ''}>
                <react_router_1.Link to={recreateRoute_1.default('data-filters/', tslib_1.__assign(tslib_1.__assign({}, this.props), { stepBack: -1 }))}>
                  {locale_1.t('Data Filters')}
                </react_router_1.Link>
              </li>
              <li className={filterType === 'discarded-groups' ? 'active' : ''}>
                <react_router_1.Link to={recreateRoute_1.default('discarded-groups/', tslib_1.__assign(tslib_1.__assign({}, this.props), { stepBack: -1 }))}>
                  {locale_1.t('Discarded Issues')}
                </react_router_1.Link>
              </li>
            </navTabs_1.default>)}

          {filterType === 'discarded-groups' ? (<groupTombstones_1.default orgId={orgId} projectId={project.slug} location={location}/>) : (<projectFiltersSettings_1.default project={project} params={this.props.params} features={features}/>)}
        </div>
      </react_1.Fragment>);
    };
    return ProjectFilters;
}(react_1.Component));
exports.default = ProjectFilters;
//# sourceMappingURL=index.jsx.map
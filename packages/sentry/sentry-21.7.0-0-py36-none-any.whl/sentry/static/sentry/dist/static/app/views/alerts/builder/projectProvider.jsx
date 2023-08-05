Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var members_1 = require("app/actionCreators/members");
var alert_1 = tslib_1.__importDefault(require("app/components/alert"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var projects_1 = tslib_1.__importDefault(require("app/utils/projects"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var scrollToTop_1 = tslib_1.__importDefault(require("app/views/settings/components/scrollToTop"));
function AlertBuilderProjectProvider(props) {
    var children = props.children, params = props.params, organization = props.organization, api = props.api, other = tslib_1.__rest(props, ["children", "params", "organization", "api"]);
    var projectId = params.projectId;
    return (<projects_1.default orgId={organization.slug} allProjects>
      {function (_a) {
            var projects = _a.projects, initiallyLoaded = _a.initiallyLoaded, isIncomplete = _a.isIncomplete;
            if (!initiallyLoaded) {
                return <loadingIndicator_1.default />;
            }
            var project = projects.find(function (_a) {
                var slug = _a.slug;
                return slug === projectId;
            });
            // if loaded, but project fetching states incomplete or project can't be found, project doesn't exist
            if (isIncomplete || !project) {
                return (<alert_1.default type="warning">
              {locale_1.t('The project you were looking for was not found.')}
            </alert_1.default>);
            }
            // fetch members list for mail action fields
            members_1.fetchOrgMembers(api, organization.slug, [project.id]);
            return (<scrollToTop_1.default location={props.location} disable={function () { return false; }}>
            {children && React.isValidElement(children)
                    ? React.cloneElement(children, tslib_1.__assign(tslib_1.__assign(tslib_1.__assign({}, other), children.props), { project: project, organization: organization }))
                    : children}
          </scrollToTop_1.default>);
        }}
    </projects_1.default>);
}
exports.default = withApi_1.default(AlertBuilderProjectProvider);
//# sourceMappingURL=projectProvider.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var create_react_class_1 = tslib_1.__importDefault(require("create-react-class"));
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var latestContextStore_1 = tslib_1.__importDefault(require("app/stores/latestContextStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var withOrganizations_1 = tslib_1.__importDefault(require("app/utils/withOrganizations"));
var withLatestContext = function (WrappedComponent) {
    return withOrganizations_1.default(create_react_class_1.default({
        displayName: "withLatestContext(" + getDisplayName_1.default(WrappedComponent) + ")",
        mixins: [reflux_1.default.connect(latestContextStore_1.default, 'latestContext')],
        render: function () {
            var organizations = this.props.organizations;
            var latestContext = this.state.latestContext;
            var _a = latestContext || {}, organization = _a.organization, project = _a.project, lastRoute = _a.lastRoute;
            // Even though org details exists in LatestContextStore,
            // fetch organization from OrganizationsStore so that we can
            // expect consistent data structure because OrganizationsStore has a list
            // of orgs but not full org details
            var latestOrganization = organization ||
                (organizations && organizations.length
                    ? organizations.find(function (_a) {
                        var slug = _a.slug;
                        return slug === configStore_1.default.get('lastOrganization');
                    }) || organizations[0]
                    : null);
            // TODO(billy): Below is going to be wrong if component is passed project, it will override
            // project from `latestContext`
            return (<WrappedComponent organizations={organizations} project={project} lastRoute={lastRoute} {...this.props} organization={(this.props.organization || latestOrganization)}/>);
        },
    }));
};
exports.default = withLatestContext;
//# sourceMappingURL=withLatestContext.jsx.map
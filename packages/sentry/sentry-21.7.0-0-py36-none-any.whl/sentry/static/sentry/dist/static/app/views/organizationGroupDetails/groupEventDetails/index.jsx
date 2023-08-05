Object.defineProperty(exports, "__esModule", { value: true });
exports.GroupEventDetailsContainer = void 0;
var tslib_1 = require("tslib");
var react_1 = require("react");
var environments_1 = require("app/actionCreators/environments");
var loadingError_1 = tslib_1.__importDefault(require("app/components/loadingError"));
var loadingIndicator_1 = tslib_1.__importDefault(require("app/components/loadingIndicator"));
var locale_1 = require("app/locale");
var organizationEnvironmentsStore_1 = tslib_1.__importDefault(require("app/stores/organizationEnvironmentsStore"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withGlobalSelection_1 = tslib_1.__importDefault(require("app/utils/withGlobalSelection"));
var withOrganization_1 = tslib_1.__importDefault(require("app/utils/withOrganization"));
var groupEventDetails_1 = tslib_1.__importDefault(require("./groupEventDetails"));
var GroupEventDetailsContainer = /** @class */ (function (_super) {
    tslib_1.__extends(GroupEventDetailsContainer, _super);
    function GroupEventDetailsContainer() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = organizationEnvironmentsStore_1.default.get();
        return _this;
    }
    GroupEventDetailsContainer.prototype.componentDidMount = function () {
        var _this = this;
        this.environmentUnsubscribe = organizationEnvironmentsStore_1.default.listen(function (data) { return _this.setState(data); }, undefined);
        var _a = organizationEnvironmentsStore_1.default.get(), environments = _a.environments, error = _a.error;
        if (!environments && !error) {
            environments_1.fetchOrganizationEnvironments(this.props.api, this.props.organization.slug);
        }
    };
    GroupEventDetailsContainer.prototype.componentWillUnmount = function () {
        if (this.environmentUnsubscribe) {
            this.environmentUnsubscribe();
        }
    };
    GroupEventDetailsContainer.prototype.render = function () {
        if (this.state.error) {
            return (<loadingError_1.default message={locale_1.t("There was an error loading your organization's environments")}/>);
        }
        // null implies loading state
        if (!this.state.environments) {
            return <loadingIndicator_1.default />;
        }
        var _a = this.props, selection = _a.selection, otherProps = tslib_1.__rest(_a, ["selection"]);
        var environments = this.state.environments.filter(function (env) {
            return selection.environments.includes(env.name);
        });
        return <groupEventDetails_1.default {...otherProps} environments={environments}/>;
    };
    return GroupEventDetailsContainer;
}(react_1.Component));
exports.GroupEventDetailsContainer = GroupEventDetailsContainer;
exports.default = withApi_1.default(withOrganization_1.default(withGlobalSelection_1.default(GroupEventDetailsContainer)));
//# sourceMappingURL=index.jsx.map
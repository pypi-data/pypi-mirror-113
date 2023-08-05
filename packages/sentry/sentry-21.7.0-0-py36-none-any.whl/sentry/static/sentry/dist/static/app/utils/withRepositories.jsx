Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var repositories_1 = require("app/actionCreators/repositories");
var repositoryActions_1 = tslib_1.__importDefault(require("app/actions/repositoryActions"));
var repositoryStore_1 = tslib_1.__importDefault(require("app/stores/repositoryStore"));
var getDisplayName_1 = tslib_1.__importDefault(require("app/utils/getDisplayName"));
var INITIAL_STATE = {
    repositories: undefined,
    repositoriesLoading: undefined,
    repositoriesError: undefined,
};
function withRepositories(WrappedComponent) {
    var WithRepositories = /** @class */ (function (_super) {
        tslib_1.__extends(WithRepositories, _super);
        function WithRepositories(props, context) {
            var _this = _super.call(this, props, context) || this;
            _this.unsubscribe = repositoryStore_1.default.listen(function () { return _this.onStoreUpdate(); }, undefined);
            var organization = _this.props.organization;
            var orgSlug = organization.slug;
            var repoData = repositoryStore_1.default.get();
            if (repoData.orgSlug !== orgSlug) {
                repositoryActions_1.default.resetRepositories();
            }
            _this.state =
                repoData.orgSlug === orgSlug
                    ? tslib_1.__assign(tslib_1.__assign({}, INITIAL_STATE), repoData) : tslib_1.__assign({}, INITIAL_STATE);
            return _this;
        }
        WithRepositories.prototype.componentDidMount = function () {
            // XXX(leedongwei): Do not move this function call unless you modify the
            // unit test named "prevents repeated calls"
            this.fetchRepositories();
        };
        WithRepositories.prototype.componentWillUnmount = function () {
            this.unsubscribe();
        };
        WithRepositories.prototype.fetchRepositories = function () {
            var _a = this.props, api = _a.api, organization = _a.organization;
            var orgSlug = organization.slug;
            var repoData = repositoryStore_1.default.get();
            // XXX(leedongwei): Do not check the orgSlug here. It would have been
            // verified at `getInitialState`. The short-circuit hack in actionCreator
            // does not update the orgSlug in the store.
            if ((!repoData.repositories && !repoData.repositoriesLoading) ||
                repoData.repositoriesError) {
                repositories_1.getRepositories(api, { orgSlug: orgSlug });
            }
        };
        WithRepositories.prototype.onStoreUpdate = function () {
            var repoData = repositoryStore_1.default.get();
            this.setState(tslib_1.__assign({}, repoData));
        };
        WithRepositories.prototype.render = function () {
            return <WrappedComponent {...this.props} {...this.state}/>;
        };
        WithRepositories.displayName = "withRepositories(" + getDisplayName_1.default(WrappedComponent) + ")";
        return WithRepositories;
    }(React.Component));
    return WithRepositories;
}
exports.default = withRepositories;
//# sourceMappingURL=withRepositories.jsx.map
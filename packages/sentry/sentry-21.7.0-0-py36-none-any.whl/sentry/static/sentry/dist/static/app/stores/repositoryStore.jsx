Object.defineProperty(exports, "__esModule", { value: true });
exports.RepositoryStoreConfig = void 0;
var tslib_1 = require("tslib");
var reflux_1 = tslib_1.__importDefault(require("reflux"));
var repositoryActions_1 = tslib_1.__importDefault(require("app/actions/repositoryActions"));
exports.RepositoryStoreConfig = {
    listenables: repositoryActions_1.default,
    state: {
        orgSlug: undefined,
        repositories: undefined,
        repositoriesLoading: undefined,
        repositoriesError: undefined,
    },
    init: function () {
        this.resetRepositories();
    },
    resetRepositories: function () {
        this.state = {
            orgSlug: undefined,
            repositories: undefined,
            repositoriesLoading: undefined,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositories: function (orgSlug) {
        this.state = {
            orgSlug: orgSlug,
            repositories: orgSlug === this.state.orgSlug ? this.state.repositories : undefined,
            repositoriesLoading: true,
            repositoriesError: undefined,
        };
        this.trigger(this.state);
    },
    loadRepositoriesError: function (err) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { repositories: undefined, repositoriesLoading: false, repositoriesError: err });
        this.trigger(this.state);
    },
    loadRepositoriesSuccess: function (data) {
        this.state = tslib_1.__assign(tslib_1.__assign({}, this.state), { repositories: data, repositoriesLoading: false, repositoriesError: undefined });
        this.trigger(this.state);
    },
    get: function () {
        return tslib_1.__assign({}, this.state);
    },
};
var RepositoryStore = reflux_1.default.createStore(exports.RepositoryStoreConfig);
exports.default = RepositoryStore;
//# sourceMappingURL=repositoryStore.jsx.map
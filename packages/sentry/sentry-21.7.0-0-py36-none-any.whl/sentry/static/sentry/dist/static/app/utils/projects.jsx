Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var memoize_1 = tslib_1.__importDefault(require("lodash/memoize"));
var partition_1 = tslib_1.__importDefault(require("lodash/partition"));
var uniqBy_1 = tslib_1.__importDefault(require("lodash/uniqBy"));
var projectActions_1 = tslib_1.__importDefault(require("app/actions/projectActions"));
var projectsStore_1 = tslib_1.__importDefault(require("app/stores/projectsStore"));
var utils_1 = require("app/utils");
var parseLinkHeader_1 = tslib_1.__importDefault(require("app/utils/parseLinkHeader"));
var withApi_1 = tslib_1.__importDefault(require("app/utils/withApi"));
var withProjects_1 = tslib_1.__importDefault(require("app/utils/withProjects"));
/**
 * This is a utility component that should be used to fetch an organization's projects (summary).
 * It can either fetch explicit projects (e.g. via slug) or a paginated list of projects.
 * These will be passed down to the render prop (`children`).
 *
 * The legacy way of handling this is that `ProjectSummary[]` is expected to be included in an
 * `Organization` as well as being saved to `ProjectsStore`.
 */
var Projects = /** @class */ (function (_super) {
    tslib_1.__extends(Projects, _super);
    function Projects() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fetchedProjects: [],
            projectsFromStore: [],
            initiallyLoaded: false,
            fetching: false,
            isIncomplete: null,
            hasMore: null,
            prevSearch: null,
            nextCursor: null,
            fetchError: null,
        };
        /**
         * List of projects that need to be fetched via API
         */
        _this.fetchQueue = new Set();
        /**
         * Memoized function that returns a `Map<project.slug, project>`
         */
        _this.getProjectsMap = memoize_1.default(function (projects) { return new Map(projects.map(function (project) { return [project.slug, project]; })); });
        /**
         * When `props.slugs` is included, identifies what projects we already
         * have summaries for and what projects need to be fetched from API
         */
        _this.loadSpecificProjects = function () {
            var _a = _this.props, slugs = _a.slugs, projects = _a.projects;
            var projectsMap = _this.getProjectsMap(projects);
            // Split slugs into projects that are in store and not in store
            // (so we can request projects not in store)
            var _b = tslib_1.__read(partition_1.default(slugs, function (slug) { return projectsMap.has(slug); }), 2), inStore = _b[0], notInStore = _b[1];
            // Get the actual summaries of projects that are in store
            var projectsFromStore = inStore.map(function (slug) { return projectsMap.get(slug); }).filter(utils_1.defined);
            // Add to queue
            notInStore.forEach(function (slug) { return _this.fetchQueue.add(slug); });
            _this.setState({
                // placeholders for projects we need to fetch
                fetchedProjects: notInStore.map(function (slug) { return ({ slug: slug }); }),
                // set initallyLoaded if any projects were fetched from store
                initiallyLoaded: !!inStore.length,
                projectsFromStore: projectsFromStore,
            });
            if (!notInStore.length) {
                return;
            }
            _this.fetchSpecificProjects();
        };
        /**
         * These will fetch projects via API (using project slug) provided by `this.fetchQueue`
         */
        _this.fetchSpecificProjects = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, orgId, passthroughPlaceholderProject, projects, fetchError, results, err_1, projectsMap, projectsOrPlaceholder;
            return tslib_1.__generator(this, function (_b) {
                switch (_b.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, passthroughPlaceholderProject = _a.passthroughPlaceholderProject;
                        if (!this.fetchQueue.size) {
                            return [2 /*return*/];
                        }
                        this.setState({
                            fetching: true,
                        });
                        projects = [];
                        fetchError = null;
                        _b.label = 1;
                    case 1:
                        _b.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchProjects(api, orgId, {
                                slugs: Array.from(this.fetchQueue),
                            })];
                    case 2:
                        results = (_b.sent()).results;
                        projects = results;
                        return [3 /*break*/, 4];
                    case 3:
                        err_1 = _b.sent();
                        console.error(err_1); // eslint-disable-line no-console
                        fetchError = err_1;
                        return [3 /*break*/, 4];
                    case 4:
                        projectsMap = this.getProjectsMap(projects);
                        projectsOrPlaceholder = Array.from(this.fetchQueue)
                            .map(function (slug) {
                            return projectsMap.has(slug)
                                ? projectsMap.get(slug)
                                : !!passthroughPlaceholderProject
                                    ? { slug: slug }
                                    : null;
                        })
                            .filter(utils_1.defined);
                        this.setState({
                            fetchedProjects: projectsOrPlaceholder,
                            isIncomplete: this.fetchQueue.size !== projects.length,
                            initiallyLoaded: true,
                            fetching: false,
                            fetchError: fetchError,
                        });
                        this.fetchQueue.clear();
                        return [2 /*return*/];
                }
            });
        }); };
        /**
         * If `props.slugs` is not provided, request from API a list of paginated project summaries
         * that are in `prop.orgId`.
         *
         * Provide render prop with results as well as `hasMore` to indicate there are more results.
         * Downstream consumers should use this to notify users so that they can e.g. narrow down
         * results using search
         */
        _this.loadAllProjects = function () { return tslib_1.__awaiter(_this, void 0, void 0, function () {
            var _a, api, orgId, limit, allProjects, _b, results, hasMore, nextCursor, err_2;
            return tslib_1.__generator(this, function (_c) {
                switch (_c.label) {
                    case 0:
                        _a = this.props, api = _a.api, orgId = _a.orgId, limit = _a.limit, allProjects = _a.allProjects;
                        this.setState({
                            fetching: true,
                        });
                        _c.label = 1;
                    case 1:
                        _c.trys.push([1, 3, , 4]);
                        return [4 /*yield*/, fetchProjects(api, orgId, {
                                limit: limit,
                                allProjects: allProjects,
                            })];
                    case 2:
                        _b = _c.sent(), results = _b.results, hasMore = _b.hasMore, nextCursor = _b.nextCursor;
                        this.setState({
                            fetching: false,
                            fetchedProjects: results,
                            initiallyLoaded: true,
                            hasMore: hasMore,
                            nextCursor: nextCursor,
                        });
                        return [3 /*break*/, 4];
                    case 3:
                        err_2 = _c.sent();
                        console.error(err_2); // eslint-disable-line no-console
                        this.setState({
                            fetching: false,
                            fetchedProjects: [],
                            initiallyLoaded: true,
                            fetchError: err_2,
                        });
                        return [3 /*break*/, 4];
                    case 4: return [2 /*return*/];
                }
            });
        }); };
        /**
         * This is an action provided to consumers for them to update the current projects
         * result set using a simple search query. You can allow the new results to either
         * be appended or replace the existing results.
         *
         * @param {String} search The search term to use
         * @param {Object} options Options object
         * @param {Boolean} options.append Results should be appended to existing list (otherwise, will replace)
         */
        _this.handleSearch = function (search, _a) {
            var _b = _a === void 0 ? {} : _a, append = _b.append;
            return tslib_1.__awaiter(_this, void 0, void 0, function () {
                var _c, api, orgId, limit, prevSearch, cursor, _d, results_1, hasMore_1, nextCursor_1, err_3;
                return tslib_1.__generator(this, function (_e) {
                    switch (_e.label) {
                        case 0:
                            _c = this.props, api = _c.api, orgId = _c.orgId, limit = _c.limit;
                            prevSearch = this.state.prevSearch;
                            cursor = this.state.nextCursor;
                            this.setState({ fetching: true });
                            _e.label = 1;
                        case 1:
                            _e.trys.push([1, 3, , 4]);
                            return [4 /*yield*/, fetchProjects(api, orgId, {
                                    search: search,
                                    limit: limit,
                                    prevSearch: prevSearch,
                                    cursor: cursor,
                                })];
                        case 2:
                            _d = _e.sent(), results_1 = _d.results, hasMore_1 = _d.hasMore, nextCursor_1 = _d.nextCursor;
                            this.setState(function (state) {
                                var fetchedProjects;
                                if (append) {
                                    // Remove duplicates
                                    fetchedProjects = uniqBy_1.default(tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(state.fetchedProjects)), tslib_1.__read(results_1)), function (_a) {
                                        var slug = _a.slug;
                                        return slug;
                                    });
                                }
                                else {
                                    fetchedProjects = results_1;
                                }
                                return {
                                    fetchedProjects: fetchedProjects,
                                    hasMore: hasMore_1,
                                    fetching: false,
                                    prevSearch: search,
                                    nextCursor: nextCursor_1,
                                };
                            });
                            return [3 /*break*/, 4];
                        case 3:
                            err_3 = _e.sent();
                            console.error(err_3); // eslint-disable-line no-console
                            this.setState({
                                fetching: false,
                                fetchError: err_3,
                            });
                            return [3 /*break*/, 4];
                        case 4: return [2 /*return*/];
                    }
                });
            });
        };
        return _this;
    }
    Projects.prototype.componentDidMount = function () {
        var slugs = this.props.slugs;
        if (slugs && !!slugs.length) {
            this.loadSpecificProjects();
        }
        else {
            this.loadAllProjects();
        }
    };
    Projects.prototype.render = function () {
        var _a = this.props, slugs = _a.slugs, children = _a.children;
        var renderProps = {
            // We want to make sure that at the minimum, we return a list of objects with only `slug`
            // while we load actual project data
            projects: this.state.initiallyLoaded
                ? tslib_1.__spreadArray(tslib_1.__spreadArray([], tslib_1.__read(this.state.fetchedProjects)), tslib_1.__read(this.state.projectsFromStore)) : (slugs && slugs.map(function (slug) { return ({ slug: slug }); })) || [],
            // This is set when we fail to find some slugs from both store and API
            isIncomplete: this.state.isIncomplete,
            // This is state for when fetching data from API
            fetching: this.state.fetching,
            // Project results (from API) are paginated and there are more projects
            // that are not in the initial queryset
            hasMore: this.state.hasMore,
            // Calls API and searches for project, accepts a callback function with signature:
            //
            // fn(searchTerm, {append: bool})
            onSearch: this.handleSearch,
            // Reflects whether or not the initial fetch for the requested projects
            // was fulfilled
            initiallyLoaded: this.state.initiallyLoaded,
            // The error that occurred if fetching failed
            fetchError: this.state.fetchError,
        };
        return children(renderProps);
    };
    Projects.defaultProps = {
        passthroughPlaceholderProject: true,
    };
    return Projects;
}(React.Component));
exports.default = withProjects_1.default(withApi_1.default(Projects));
function fetchProjects(api, orgId, _a) {
    var _b = _a === void 0 ? {} : _a, slugs = _b.slugs, search = _b.search, limit = _b.limit, prevSearch = _b.prevSearch, cursor = _b.cursor, allProjects = _b.allProjects;
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var query, _c, loading, projects, hasMore, nextCursor, _d, results, xhr, pageLinks, paginationObject;
        return tslib_1.__generator(this, function (_e) {
            switch (_e.label) {
                case 0:
                    query = {
                        // Never return latestDeploys project property from api
                        collapse: ['latestDeploys'],
                    };
                    if (slugs && slugs.length) {
                        query.query = slugs.map(function (slug) { return "slug:" + slug; }).join(' ');
                    }
                    if (search) {
                        query.query = "" + (query.query ? query.query + " " : '') + search;
                    }
                    if (((!prevSearch && !search) || prevSearch === search) && cursor) {
                        query.cursor = cursor;
                    }
                    // "0" shouldn't be a valid value, so this check is fine
                    if (limit) {
                        query.per_page = limit;
                    }
                    if (allProjects) {
                        _c = projectsStore_1.default.getState(), loading = _c.loading, projects = _c.projects;
                        // If the projects store is loaded then return all projects from the store
                        if (!loading) {
                            return [2 /*return*/, {
                                    results: projects,
                                    hasMore: false,
                                }];
                        }
                        // Otherwise mark the query to fetch all projects from the API
                        query.all_projects = 1;
                    }
                    hasMore = false;
                    nextCursor = null;
                    return [4 /*yield*/, api.requestPromise("/organizations/" + orgId + "/projects/", {
                            includeAllArgs: true,
                            query: query,
                        })];
                case 1:
                    _d = tslib_1.__read.apply(void 0, [_e.sent(), 3]), results = _d[0], xhr = _d[2];
                    pageLinks = xhr && xhr.getResponseHeader('Link');
                    if (pageLinks) {
                        paginationObject = parseLinkHeader_1.default(pageLinks);
                        hasMore =
                            paginationObject &&
                                (paginationObject.next.results || paginationObject.previous.results);
                        nextCursor = paginationObject.next.cursor;
                    }
                    // populate the projects store if all projects were fetched
                    if (allProjects) {
                        projectActions_1.default.loadProjects(results);
                    }
                    return [2 /*return*/, {
                            results: results,
                            hasMore: hasMore,
                            nextCursor: nextCursor,
                        }];
            }
        });
    });
}
//# sourceMappingURL=projects.jsx.map
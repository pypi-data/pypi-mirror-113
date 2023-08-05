Object.defineProperty(exports, "__esModule", { value: true });
exports.RouteSource = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var flattenDepth_1 = tslib_1.__importDefault(require("lodash/flattenDepth"));
var createFuzzySearch_1 = require("app/utils/createFuzzySearch");
var replaceRouterParams_1 = tslib_1.__importDefault(require("app/utils/replaceRouterParams"));
var withLatestContext_1 = tslib_1.__importDefault(require("app/utils/withLatestContext"));
var navigationConfiguration_1 = tslib_1.__importDefault(require("app/views/settings/account/navigationConfiguration"));
var navigationConfiguration_2 = tslib_1.__importDefault(require("app/views/settings/organization/navigationConfiguration"));
var navigationConfiguration_3 = tslib_1.__importDefault(require("app/views/settings/project/navigationConfiguration"));
/**
 * navigation configuration can currently be either:
 *
 *  - an array of {name: string, items: Array<{NavItem}>} OR
 *  - a function that returns the above
 *    (some navigation items require additional context, e.g. a badge based on
 *    a `project` property)
 *
 * We need to go through all navigation configurations and get a flattened list
 * of all navigation item objects
 */
var mapFunc = function (config, context) {
    if (context === void 0) { context = null; }
    return (Array.isArray(config) ? config : context !== null ? config(context) : []).map(function (_a) {
        var items = _a.items;
        return items.filter(function (_a) {
            var show = _a.show;
            return typeof show === 'function' && context !== null ? show(context) : true;
        });
    });
};
var RouteSource = /** @class */ (function (_super) {
    tslib_1.__extends(RouteSource, _super);
    function RouteSource() {
        var _this = _super !== null && _super.apply(this, arguments) || this;
        _this.state = {
            fuzzy: undefined,
        };
        return _this;
    }
    RouteSource.prototype.componentDidMount = function () {
        this.createSearch();
    };
    RouteSource.prototype.componentDidUpdate = function (prevProps) {
        if (prevProps.project === this.props.project &&
            prevProps.organization === this.props.organization) {
            return;
        }
        this.createSearch();
    };
    RouteSource.prototype.createSearch = function () {
        var _a, _b;
        return tslib_1.__awaiter(this, void 0, void 0, function () {
            var _c, project, organization, context, searchMap, options, fuzzy;
            return tslib_1.__generator(this, function (_d) {
                switch (_d.label) {
                    case 0:
                        _c = this.props, project = _c.project, organization = _c.organization;
                        context = {
                            project: project,
                            organization: organization,
                            access: new Set((_a = organization === null || organization === void 0 ? void 0 : organization.access) !== null && _a !== void 0 ? _a : []),
                            features: new Set((_b = project === null || project === void 0 ? void 0 : project.features) !== null && _b !== void 0 ? _b : []),
                        };
                        searchMap = flattenDepth_1.default([
                            mapFunc(navigationConfiguration_1.default, context),
                            mapFunc(navigationConfiguration_3.default, context),
                            mapFunc(navigationConfiguration_2.default, context),
                        ], 2);
                        options = tslib_1.__assign(tslib_1.__assign({}, this.props.searchOptions), { keys: ['title', 'description'] });
                        return [4 /*yield*/, createFuzzySearch_1.createFuzzySearch(searchMap !== null && searchMap !== void 0 ? searchMap : [], options)];
                    case 1:
                        fuzzy = _d.sent();
                        this.setState({ fuzzy: fuzzy });
                        return [2 /*return*/];
                }
            });
        });
    };
    RouteSource.prototype.render = function () {
        var _a, _b;
        var _c = this.props, query = _c.query, params = _c.params, children = _c.children;
        var results = (_b = (_a = this.state.fuzzy) === null || _a === void 0 ? void 0 : _a.search(query).map(function (_a) {
            var item = _a.item, rest = tslib_1.__rest(_a, ["item"]);
            return (tslib_1.__assign({ item: tslib_1.__assign(tslib_1.__assign({}, item), { sourceType: 'route', resultType: 'route', to: replaceRouterParams_1.default(item.path, params) }) }, rest));
        })) !== null && _b !== void 0 ? _b : [];
        return children({
            isLoading: this.state.fuzzy === undefined,
            results: results,
        });
    };
    RouteSource.defaultProps = {
        searchOptions: {},
    };
    return RouteSource;
}(React.Component));
exports.RouteSource = RouteSource;
exports.default = withLatestContext_1.default(RouteSource);
//# sourceMappingURL=routeSource.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var isEqual_1 = tslib_1.__importDefault(require("lodash/isEqual"));
var globalSelection_1 = require("app/actionCreators/globalSelection");
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var utils_1 = require("./utils");
var getDateObjectFromQuery = function (query) {
    return Object.fromEntries(Object.entries(query).filter(function (_a) {
        var _b = tslib_1.__read(_a, 1), key = _b[0];
        return globalSelectionHeader_1.DATE_TIME_KEYS.includes(key);
    }));
};
/**
 * Initializes GlobalSelectionHeader
 *
 * Calls an actionCreator to load project/environment from local storage if possible,
 * otherwise populate with defaults.
 *
 * This should only happen when the header is mounted
 * e.g. when changing views or organizations.
 */
var InitializeGlobalSelectionHeader = /** @class */ (function (_super) {
    tslib_1.__extends(InitializeGlobalSelectionHeader, _super);
    function InitializeGlobalSelectionHeader() {
        return _super !== null && _super.apply(this, arguments) || this;
    }
    InitializeGlobalSelectionHeader.prototype.componentDidMount = function () {
        var _a = this.props, location = _a.location, router = _a.router, organization = _a.organization, defaultSelection = _a.defaultSelection, forceProject = _a.forceProject, memberProjects = _a.memberProjects, shouldForceProject = _a.shouldForceProject, shouldEnforceSingleProject = _a.shouldEnforceSingleProject, skipLoadLastUsed = _a.skipLoadLastUsed, showAbsolute = _a.showAbsolute;
        globalSelection_1.initializeUrlState({
            organization: organization,
            queryParams: location.query,
            router: router,
            skipLoadLastUsed: skipLoadLastUsed,
            memberProjects: memberProjects,
            defaultSelection: defaultSelection,
            forceProject: forceProject,
            shouldForceProject: shouldForceProject,
            shouldEnforceSingleProject: shouldEnforceSingleProject,
            showAbsolute: showAbsolute,
        });
    };
    InitializeGlobalSelectionHeader.prototype.componentDidUpdate = function (prevProps) {
        /**
         * This happens e.g. using browser's navigation button, in which case
         * we need to update our store to reflect URL changes
         */
        if (prevProps.location.query !== this.props.location.query) {
            var oldQuery = utils_1.getStateFromQuery(prevProps.location.query, {
                allowEmptyPeriod: true,
            });
            var newQuery = utils_1.getStateFromQuery(this.props.location.query, {
                allowEmptyPeriod: true,
            });
            var newEnvironments = newQuery.environment || [];
            var newDateObject = getDateObjectFromQuery(newQuery);
            var oldDateObject = getDateObjectFromQuery(oldQuery);
            /**
             * Do not pass router to these actionCreators, as we do not want to update
             * routes since these state changes are happening due to a change of routes
             */
            if (!isEqual_1.default(oldQuery.project, newQuery.project)) {
                globalSelection_1.updateProjects(newQuery.project || [], null, { environments: newEnvironments });
            }
            else if (!isEqual_1.default(oldQuery.environment, newQuery.environment)) {
                /**
                 * When the project stays the same, it's still possible that the environment
                 * changed, so explictly update the enviornment
                 */
                globalSelection_1.updateEnvironments(newEnvironments);
            }
            if (!isEqual_1.default(oldDateObject, newDateObject)) {
                globalSelection_1.updateDateTime(newDateObject);
            }
        }
    };
    InitializeGlobalSelectionHeader.prototype.render = function () {
        return null;
    };
    return InitializeGlobalSelectionHeader;
}(React.Component));
exports.default = InitializeGlobalSelectionHeader;
//# sourceMappingURL=initializeGlobalSelectionHeader.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
exports.getQuery = void 0;
var tslib_1 = require("tslib");
var pick_1 = tslib_1.__importDefault(require("lodash/pick"));
var qs = tslib_1.__importStar(require("query-string"));
var globalSelectionHeader_1 = require("app/constants/globalSelectionHeader");
var DEFAULT_STATUS = 'unresolved';
/**
 * Get query for API given the current location.search string
 */
function getQuery(search) {
    var query = qs.parse(search);
    var status = typeof query.status !== 'undefined' ? query.status : DEFAULT_STATUS;
    var queryParams = tslib_1.__assign({ status: status }, pick_1.default(query, tslib_1.__spreadArray(['cursor'], tslib_1.__read(Object.values(globalSelectionHeader_1.URL_PARAM)))));
    return queryParams;
}
exports.getQuery = getQuery;
//# sourceMappingURL=utils.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
exports.saveToSourceGroupData = exports.fetchSourceGroupData = void 0;
var types_1 = require("../types");
var utils_1 = require("../utils");
var localStorage_1 = require("./localStorage");
function fetchSourceGroupData() {
    var fetchedSourceGroupData = localStorage_1.fetchFromStorage();
    if (!fetchedSourceGroupData) {
        var sourceGroupData = {
            eventId: '',
            sourceSuggestions: utils_1.valueSuggestions,
        };
        localStorage_1.saveToStorage(sourceGroupData);
        return sourceGroupData;
    }
    return fetchedSourceGroupData;
}
exports.fetchSourceGroupData = fetchSourceGroupData;
function saveToSourceGroupData(eventId, sourceSuggestions) {
    if (sourceSuggestions === void 0) { sourceSuggestions = utils_1.valueSuggestions; }
    switch (eventId.status) {
        case types_1.EventIdStatus.LOADING:
            break;
        case types_1.EventIdStatus.LOADED:
            localStorage_1.saveToStorage({ eventId: eventId.value, sourceSuggestions: sourceSuggestions });
            break;
        default:
            localStorage_1.saveToStorage({ eventId: '', sourceSuggestions: sourceSuggestions });
    }
}
exports.saveToSourceGroupData = saveToSourceGroupData;
//# sourceMappingURL=utils.jsx.map
Object.defineProperty(exports, "__esModule", { value: true });
exports.loadIncidents = void 0;
var tslib_1 = require("tslib");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
function getIncidentsFromIncidentResponse(statuspageIncidents) {
    if (statuspageIncidents === null || statuspageIncidents.length === 0) {
        return { incidents: [], indicator: 'none' };
    }
    var isMajor = false;
    var incidents = [];
    statuspageIncidents.forEach(function (item) {
        if (!isMajor && item.impact === 'major') {
            isMajor = true;
        }
        incidents.push({
            id: item.id,
            name: item.name,
            updates: item.incident_updates.map(function (update) { return update.body; }),
            url: item.shortlink,
            status: item.status,
        });
    });
    return { incidents: incidents, indicator: isMajor ? 'major' : 'minor' };
}
function loadIncidents() {
    return tslib_1.__awaiter(this, void 0, void 0, function () {
        var cfg, response, data, _a, incidents, indicator;
        return tslib_1.__generator(this, function (_b) {
            switch (_b.label) {
                case 0:
                    cfg = configStore_1.default.get('statuspage');
                    if (!cfg || !cfg.id) {
                        return [2 /*return*/, null];
                    }
                    return [4 /*yield*/, fetch("https://" + cfg.id + "." + cfg.api_host + "/api/v2/incidents/unresolved.json")];
                case 1:
                    response = _b.sent();
                    if (!response.ok) {
                        return [2 /*return*/, null];
                    }
                    return [4 /*yield*/, response.json()];
                case 2:
                    data = _b.sent();
                    _a = getIncidentsFromIncidentResponse(data.incidents), incidents = _a.incidents, indicator = _a.indicator;
                    return [2 /*return*/, {
                            incidents: incidents,
                            indicator: indicator,
                            url: data.page.url,
                        }];
            }
        });
    });
}
exports.loadIncidents = loadIncidents;
//# sourceMappingURL=serviceIncidents.jsx.map
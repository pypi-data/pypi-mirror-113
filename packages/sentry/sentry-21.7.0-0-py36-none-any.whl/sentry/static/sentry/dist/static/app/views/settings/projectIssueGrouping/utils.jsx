Object.defineProperty(exports, "__esModule", { value: true });
exports.getGroupingRisk = exports.getGroupingChanges = void 0;
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var locale_1 = require("app/locale");
function getGroupingChanges(project, groupingConfigs) {
    var _a, _b;
    var byId = {};
    var updateNotes = '';
    var riskLevel = 0;
    var latestGroupingConfig = null;
    groupingConfigs.forEach(function (cfg) {
        byId[cfg.id] = cfg;
        if (cfg.latest && project.groupingConfig !== cfg.id) {
            updateNotes = cfg.changelog;
            latestGroupingConfig = cfg;
            riskLevel = cfg.risk;
        }
    });
    if (latestGroupingConfig) {
        var next = (_a = latestGroupingConfig.base) !== null && _a !== void 0 ? _a : '';
        while (next !== project.groupingConfig) {
            var cfg = byId[next];
            if (!cfg) {
                break;
            }
            riskLevel = Math.max(riskLevel, cfg.risk);
            updateNotes = cfg.changelog + '\n' + updateNotes;
            next = (_b = cfg.base) !== null && _b !== void 0 ? _b : '';
        }
    }
    return { updateNotes: updateNotes, riskLevel: riskLevel, latestGroupingConfig: latestGroupingConfig };
}
exports.getGroupingChanges = getGroupingChanges;
function getGroupingRisk(riskLevel) {
    switch (riskLevel) {
        case 0:
            return {
                riskNote: locale_1.t('This upgrade has the chance to create some new issues.'),
                alertType: 'info',
            };
        case 1:
            return {
                riskNote: locale_1.t('This upgrade will create some new issues.'),
                alertType: 'warning',
            };
        case 2:
            return {
                riskNote: (<strong>
            {locale_1.t('The new grouping strategy is incompatible with the current and will create entirely new issues.')}
          </strong>),
                alertType: 'error',
            };
        default:
            return { riskNote: undefined, alertType: undefined };
    }
}
exports.getGroupingRisk = getGroupingRisk;
//# sourceMappingURL=utils.jsx.map
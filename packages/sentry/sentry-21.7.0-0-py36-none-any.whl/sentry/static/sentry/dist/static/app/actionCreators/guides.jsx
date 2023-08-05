Object.defineProperty(exports, "__esModule", { value: true });
exports.recordDismiss = exports.recordFinish = exports.dismissGuide = exports.closeGuide = exports.toStep = exports.nextStep = exports.unregisterAnchor = exports.registerAnchor = exports.fetchGuides = void 0;
var tslib_1 = require("tslib");
var guideActions_1 = tslib_1.__importDefault(require("app/actions/guideActions"));
var api_1 = require("app/api");
var configStore_1 = tslib_1.__importDefault(require("app/stores/configStore"));
var analytics_1 = require("app/utils/analytics");
var api = new api_1.Client();
function fetchGuides() {
    api.request('/assistant/?v2', {
        method: 'GET',
        success: function (data) {
            guideActions_1.default.fetchSucceeded(data);
        },
    });
}
exports.fetchGuides = fetchGuides;
function registerAnchor(target) {
    guideActions_1.default.registerAnchor(target);
}
exports.registerAnchor = registerAnchor;
function unregisterAnchor(target) {
    guideActions_1.default.unregisterAnchor(target);
}
exports.unregisterAnchor = unregisterAnchor;
function nextStep() {
    guideActions_1.default.nextStep();
}
exports.nextStep = nextStep;
function toStep(step) {
    guideActions_1.default.toStep(step);
}
exports.toStep = toStep;
function closeGuide(dismissed) {
    guideActions_1.default.closeGuide(dismissed);
}
exports.closeGuide = closeGuide;
function dismissGuide(guide, step, orgId) {
    recordDismiss(guide, step, orgId);
    closeGuide(true);
}
exports.dismissGuide = dismissGuide;
function recordFinish(guide, orgId) {
    api.request('/assistant/', {
        method: 'PUT',
        data: {
            guide: guide,
            status: 'viewed',
        },
    });
    var user = configStore_1.default.get('user');
    if (!user) {
        return;
    }
    var data = {
        eventKey: 'assistant.guide_finished',
        eventName: 'Assistant Guide Finished',
        guide: guide,
        organization_id: orgId,
        user_id: parseInt(user.id, 10),
    };
    analytics_1.trackAnalyticsEvent(data);
}
exports.recordFinish = recordFinish;
function recordDismiss(guide, step, orgId) {
    api.request('/assistant/', {
        method: 'PUT',
        data: {
            guide: guide,
            status: 'dismissed',
        },
    });
    var user = configStore_1.default.get('user');
    if (!user) {
        return;
    }
    var data = {
        eventKey: 'assistant.guide_dismissed',
        eventName: 'Assistant Guide Dismissed',
        guide: guide,
        step: step,
        organization_id: orgId,
        user_id: parseInt(user.id, 10),
    };
    analytics_1.trackAnalyticsEvent(data);
}
exports.recordDismiss = recordDismiss;
//# sourceMappingURL=guides.jsx.map
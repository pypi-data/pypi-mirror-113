Object.defineProperty(exports, "__esModule", { value: true });
var tslib_1 = require("tslib");
var React = tslib_1.__importStar(require("react"));
var qs = tslib_1.__importStar(require("query-string"));
var integrationUtil_1 = require("app/utils/integrationUtil");
var platform_1 = tslib_1.__importDefault(require("./platform"));
var platformIntegrationSetup_1 = tslib_1.__importDefault(require("./platformIntegrationSetup"));
var PlatformOrIntegration = function (props) {
    var parsed = qs.parse(window.location.search);
    var platform = props.params.platform;
    var integrationSlug = platform && integrationUtil_1.platfromToIntegrationMap[platform];
    // check for manual override query param
    if (integrationSlug && parsed.manual !== '1') {
        return <platformIntegrationSetup_1.default integrationSlug={integrationSlug} {...props}/>;
    }
    return <platform_1.default {...props}/>;
};
exports.default = PlatformOrIntegration;
//# sourceMappingURL=platformOrIntegration.jsx.map
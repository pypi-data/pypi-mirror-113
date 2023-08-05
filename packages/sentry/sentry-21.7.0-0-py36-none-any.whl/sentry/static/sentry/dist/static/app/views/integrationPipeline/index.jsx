function integrationPipeline() {
    return __awaiter(this, void 0, void 0, function () {
        var init;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, Promise.resolve().then(function () { return __importStar(require('./init')); })];
                case 1:
                    init = (_a.sent()).init;
                    init();
                    return [2 /*return*/];
            }
        });
    });
}
integrationPipeline();
//# sourceMappingURL=index.jsx.map